import { parse, stringify } from 'yaml';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import type { CitationFile, ZenodoMetadata, RelatedIdentifier } from '../types.js';

const CITATION_PATH = 'CITATION.cff';
const ZENODO_PATH = '.zenodo.json';
const CFFCONVERT_IMAGE = 'citationcff/cffconvert:latest';

export function updateCitationDate(version: string): void {
  if (!existsSync(CITATION_PATH)) {
    throw new Error(`CITATION.cff not found at ${CITATION_PATH}`);
  }

  const content = readFileSync(CITATION_PATH, 'utf8');
  const citation = parse(content) as CitationFile;

  citation['date-released'] = new Date().toISOString().split('T')[0];
  citation.version = version;

  writeFileSync(CITATION_PATH, stringify(citation));
  console.log(`✓ Updated date-released to ${citation['date-released']} and version to ${version}`);
}

/**
 * Generates .zenodo.json from CITATION.cff using cffconvert.
 * Preserves Zenodo-specific fields that are not in CFF format.
 */
export function generateZenodoJson(): void {
  if (!existsSync(CITATION_PATH)) {
    throw new Error(`CITATION.cff not found at ${CITATION_PATH}`);
  }

  console.log('  Generating .zenodo.json from CITATION.cff...');

  // Read existing .zenodo.json to preserve Zenodo-specific fields
  let existingZenodo: Partial<ZenodoMetadata> = {};
  if (existsSync(ZENODO_PATH)) {
    try {
      const existingContent = readFileSync(ZENODO_PATH, 'utf8');
      existingZenodo = JSON.parse(existingContent) as Partial<ZenodoMetadata>;
    } catch (error) {
      console.warn(`  Warning: Could not parse existing ${ZENODO_PATH}, will create new one`);
    }
  }

  // Use cffconvert via Docker to generate Zenodo JSON from CITATION.cff
  // The Docker image has cffconvert as entrypoint, so we just pass the arguments
  const dockerCmd = `docker run --rm \
    -v $(pwd):/app \
    -w /app \
    ${CFFCONVERT_IMAGE} \
    -f zenodo -i ${CITATION_PATH} -o ${ZENODO_PATH}`;

  try {
    execSync(dockerCmd, { stdio: 'inherit' });
  } catch (error) {
    throw new Error(`Failed to generate .zenodo.json: ${error}`);
  }

  // Read the generated file
  const generatedContent = readFileSync(ZENODO_PATH, 'utf8');
  const generatedRaw = JSON.parse(generatedContent) as any;

  // Normalize ORCID format in creators (cffconvert may output full URLs, Zenodo needs just the ID)
  if (generatedRaw.creators) {
    generatedRaw.creators = generatedRaw.creators.map((creator: any) => {
      if (creator.orcid) {
        // Extract ORCID ID from URL if present (e.g., "https://orcid.org/0009-0009-0935-2954" -> "0009-0009-0935-2954")
        const orcidMatch = creator.orcid.match(/(\d{4}-\d{4}-\d{4}-\d{3}[\dX])/);
        if (orcidMatch) {
          creator.orcid = orcidMatch[1];
        }
      }
      return creator;
    });
  }

  // Normalize license format (cffconvert may output {id: "CC-BY-4.0"}, Zenodo needs string)
  let normalizedLicense = 'cc-by-4.0';
  if (generatedRaw.license) {
    if (typeof generatedRaw.license === 'string') {
      normalizedLicense = generatedRaw.license.toLowerCase();
    } else if (generatedRaw.license.id) {
      normalizedLicense = generatedRaw.license.id.toLowerCase();
    }
  }

  // Preserve Zenodo-specific fields that cffconvert doesn't handle
  // These fields are not part of CFF standard but are needed for Zenodo
  const preserved: Partial<ZenodoMetadata> = {
    // Preserve upload_type and publication_type if they exist
    upload_type: existingZenodo.upload_type || 'publication',
    publication_type: existingZenodo.publication_type || 'preprint',

    // Preserve related_identifiers (not in CFF standard)
    related_identifiers: existingZenodo.related_identifiers || [
      {
        identifier: 'https://github.com/omega-pcf/01-hilbert-polya',
        relation: 'isSupplementTo',
        scheme: 'url',
        resource_type: 'software',
      },
      {
        identifier: 'https://colab.research.google.com/drive/1KExRnNtx91TjVyYD0FlcB_TLQwZB4GKq',
        relation: 'isDocumentedBy',
        scheme: 'url',
        resource_type: 'other',
      },
    ] as RelatedIdentifier[],

    // Preserve repository_url if it exists
    repository_url: existingZenodo.repository_url || generatedRaw.repository_url,

    // Preserve language (not in CFF standard, but needed for Zenodo)
    language: existingZenodo.language || 'spa',
  };

  // Build final Zenodo metadata with proper types
  const final: ZenodoMetadata = {
    title: generatedRaw.title || '',
    version: generatedRaw.version || '',
    upload_type: preserved.upload_type || 'publication',
    publication_type: preserved.publication_type,
    description: generatedRaw.description || generatedRaw.abstract || '',
    creators: generatedRaw.creators || [],
    access_right: generatedRaw.access_right || 'open',
    license: normalizedLicense,
    language: preserved.language || 'spa',
    keywords: generatedRaw.keywords || [],
    related_identifiers: preserved.related_identifiers,
    repository_url: preserved.repository_url,
  };

  // Write the final merged JSON with proper formatting
  writeFileSync(ZENODO_PATH, JSON.stringify(final, null, 2) + '\n');
  console.log(`✓ Generated ${ZENODO_PATH} from ${CITATION_PATH}`);
}

