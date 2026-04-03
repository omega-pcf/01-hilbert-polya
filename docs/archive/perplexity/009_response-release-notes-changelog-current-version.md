Basándome en la investigación exhaustiva que he realizado sobre la documentación oficial y los problemas reportados en los repositorios de `release-it` y `@release-it/conventional-changelog`, puedo proporcionarte respuestas precisas y verificadas a tus dudas.

## Solución al Problema del Changelog en GitHub Release Notes

### 1. ¿Qué contiene exactamente `context.changelog`?

Según la documentación oficial de `@release-it/conventional-changelog` y el issue #1025 que encontré, **`context.changelog` contiene solo los cambios de la versión actual**, no todo el historial del `CHANGELOG.md`.[1][2]

El flujo de trabajo es el siguiente:
1. El plugin `@release-it/conventional-changelog` se ejecuta primero
2. Lee los commits desde el último tag hasta HEAD
3. Genera **solo la sección de la versión actual** y la guarda en memoria como `context.changelog`
4. Actualiza el archivo `CHANGELOG.md` (añadiendo esta nueva sección al inicio)
5. Este `context.changelog` está disponible para las funciones de `releaseNotes`

### 2. El problema con `autoGenerate: false`

Según el issue #1025, el problema que estás experimentando es causado por tu uso de `autoGenerate: false`. Cuando esta opción está configurada como `false`, el plugin conventional-changelog **SÍ genera correctamente `context.changelog`** con solo la versión actual, pero tu comando shell `cat CHANGELOG.md` ignora esto y lee todo el archivo.[1]

**La solución correcta según la documentación oficial:**

Simplemente **elimina la línea `autoGenerate: false`** de tu configuración. Cuando usas el plugin `@release-it/conventional-changelog` sin establecer `autoGenerate`, release-it automáticamente usa el `context.changelog` generado por el plugin para las GitHub Release Notes.[1]

### 3. ¿Cómo acceder a `context.changelog` desde shell?

**No puedes acceder a `context.changelog` desde un comando shell directamente**. Las variables de contexto como `context.changelog` solo están disponibles cuando usas funciones en archivos `.release-it.js` o `.release-it.cjs`.[3]

Según la documentación oficial de GitHub Releases:[3]

> "The value can either be a string or a function but **a function is only supported when configuring release-it using `.release-it.js` or `.release-it.cjs` file**."

### 4. Forma estándar recomendada (SIN funciones)

**La forma más sencilla y estándar es NO usar `releaseNotes` personalizado cuando usas `@release-it/conventional-changelog`:**

```typescript
// .release-it.ts
github: {
  release: true,
  releaseName: 'v${version}',
  // NO incluir autoGenerate: false
  // NO incluir releaseNotes personalizado
  assets: ['build/document-v*.pdf', 'checksums.txt'],
},
plugins: {
  '@release-it/conventional-changelog': {
    preset: {
      name: 'conventionalcommits',
    },
    infile: 'CHANGELOG.md',
  },
}
```

Cuando **no** especificas `github.releaseNotes` ni `github.autoGenerate`, release-it automáticamente usa el `context.changelog` generado por el plugin conventional-changelog.[3][1]

### 5. Si necesitas personalizar las Release Notes

Si necesitas añadir información adicional (como tu DOI y sección de Files), **debes cambiar a `.release-it.cjs`** porque las funciones NO funcionan en archivos TypeScript `.ts`:[3]

**Opción A: Usar `.release-it.cjs` con función (FORMA ESTÁNDAR)**

```javascript
// .release-it.cjs
module.exports = {
  git: {
    commitMessage: 'chore: release v${version}',
    tagName: 'v${version}',
  },
  github: {
    release: true,
    releaseName: 'v${version}',
    // Función que accede a context.changelog
    releaseNotes(context) {
      // context.changelog contiene SOLO los cambios de la versión actual
      const versionChangelog = context.changelog;
      
      // Añade tu información personalizada
      return `${versionChangelog}

## Files

- **PDF**: \`build/document-v${context.version}.pdf\` - Compiled preprint document

## DOI

DOI: 10.5281/zenodo.17619486`;
    },
    assets: ['build/document-v*.pdf', 'checksums.txt'],
  },
  npm: {
    publish: false,
  },
  plugins: {
    '@release-it/conventional-changelog': {
      preset: {
        name: 'conventionalcommits',
      },
      infile: 'CHANGELOG.md',
    },
    '@release-it/bumper': {
      out: [
        { file: 'package.json', path: 'version' },
        { file: 'CITATION.cff', path: 'version' },
        { file: '.zenodo.json', path: 'version' },
      ],
    },
  },
};
```

**Opción B: Solución más simple - Sin personalización de releaseNotes**

Si tu personalización no es crítica, la forma MÁS estándar es simplemente eliminar `autoGenerate: false` y `releaseNotes` completamente:

```typescript
// .release-it.ts (mantener TypeScript)
import type { Config } from 'release-it';

export default {
  git: {
    commitMessage: 'chore: release v${version}',
    tagName: 'v${version}',
  },
  github: {
    release: true,
    releaseName: 'v${version}',
    // ¡No incluir autoGenerate ni releaseNotes!
    assets: ['build/document-v*.pdf', 'checksums.txt'],
  },
  npm: {
    publish: false,
  },
  plugins: {
    '@release-it/conventional-changelog': {
      preset: {
        name: 'conventionalcommits',
      },
      infile: 'CHANGELOG.md',
    },
    '@release-it/bumper': {
      out: [
        { file: 'package.json', path: 'version' },
        { file: 'CITATION.cff', path: 'version' },
        { file: '.zenodo.json', path: 'version' },
      ],
    },
  },
} satisfies Config;
```

Luego puedes añadir manualmente la información del DOI y los archivos después de crear el release, o usar un hook `after:release` para editar el release.

### 6. Variables de contexto disponibles

Según la documentación oficial, estas son las variables disponibles en funciones de `releaseNotes`:[4][3]

- `context.version` - Nueva versión
- `context.latestVersion` - Versión anterior
- `context.changelog` - **Changelog generado por el plugin (solo versión actual)**
- `context.name` - Nombre del paquete
- `context.repo.owner` - Propietario del repositorio
- `context.repo.repository` - Nombre del repositorio
- `context.branchName` - Nombre de la rama
- `context.latestTag` - Tag anterior
- `context.tagName` - Nuevo tag

### Resumen de la Solución Recomendada

**La forma más estándar y simple:**

1. **Elimina `autoGenerate: false`** de tu configuración actual
2. **Elimina el `releaseNotes` personalizado** (el comando shell `cat CHANGELOG.md`)
3. Release-it automáticamente usará `context.changelog` del plugin, que contiene **solo la versión actual**

Esto es exactamente lo que descubrieron otros usuarios en el issue #1025, donde el mantenedor confirmó que `autoGenerate: false` sobreescribe el changelog generado por el plugin.[1]

**Si NECESITAS personalizar las notas:**

1. **Cambia a `.release-it.cjs`** (archivo CommonJS)
2. Usa una función `releaseNotes(context)` que acceda a `context.changelog`
3. Añade tu contenido personalizado alrededor del changelog

Esta es la forma estándar y documentada oficialmente,mente, no un hack.[89]

[1](https://github.com/release-it/release-it/issues/1025)
[2](https://github.com/release-it/conventional-changelog)
[3](https://github.com/release-it/release-it/issues/1152)
[4](https://github.com/release-it/release-it/releases)
[5](https://stackoverflow.com/questions/78196255/get-release-it-to-put-each-new-commit-under-the-corresponding-release-version-in)
[6](https://github.com/release-it/release-it)
[7](https://techblog.commercetools.com/adopting-changesets-for-release-and-changelog-automation-cbdc36bbdc10)
[8](https://www.npmjs.com/package/conventional-changelog?activeTab=dependencies)
[9](https://www.arbitrary-but-fixed.net/devops/shell/2021/02/19/release-notes-from-changelog.html)
[10](https://repo.ito.gov.ir/repo/library/Npm/Others/@release-it/conventional-changelog-5.1.1.html)
[11](https://github.com/release-it/release-it/issues/585)
[12](https://common-changelog.org)
[13](https://www.pixelmatters.com/insights/conventional-commits-dynamic-changelog)
[14](https://stackoverflow.com/questions/78292078/where-is-the-changelog-and-release-notes-of-the-git-project)
[15](https://docs.gitlab.com/development/changelog/)
[16](https://www.conventionalcommits.org/en/v1.0.0/)
[17](https://azurewithaj.com/posts/devops-release-tag-generation/)
[18](https://keepachangelog.com/en/1.1.0/)
[19](https://processwire.com/talk/topic/28235-how-to-get-fully-automated-releases-tags-changelog-and-version-numbers-for-your-module-or-processwire-project/)
[20](https://www.reddit.com/r/opensource/comments/tyr0ez/i_spent_several_days_composing_a_github_release/)
[21](https://www.launchnotes.com/blog/release-notes-vs-changelog-understanding-the-key-differences-and-when-to-use-each)
[22](https://sophiabits.com/blog/conventional-changelogs-suck)
[23](https://github.com/release-it/release-it/issues/592)
[24](https://app.unpkg.com/release-it@14.8.0/files/README.md)
[25](https://rasmusp.com/tils/release-it-automation-for-versioning-and-changelog)
[26](https://dev.to/renehernandez/automate-changelog-and-releases-creation-in-github-3ajm)
[27](https://semantic-release.gitbook.io/semantic-release/support/faq)
[28](https://www.npmjs.com/package/@release-it/conventional-changelog)
[29](https://stackoverflow.com/questions/21214562/how-to-release-versions-on-github-through-the-command-line)
[30](https://npmjs.com/package/@release-it/conventional-changelog/v/3.1.0)
[31](https://www.infralovers.com/blog/2022-08-08-changelog-automation-with-github-actions/)
[32](https://github.com/orgs/community/discussions/27127)
[33](https://stackoverflow.com/questions/75679683/how-can-i-auto-generate-a-release-note-and-create-a-release-using-github-actions)
[34](https://www.npmjs.com/package/release-it/v/15.0.0)
[35](https://dev.to/devsatasurion/automate-changelogs-to-ease-your-release-282)
[36](https://github.com/marketplace/actions/release-it-github-action)
[37](https://www.weblearningblog.com/ci-cd/automate-github-releases-and-generate-release-notes-with-release-it/)
[38](https://blog.logrocket.com/using-semantic-release-automate-releases-changelogs/)
[39](https://www.npmjs.com/package/release-it)
[40](https://github.com/release-it/keep-a-changelog)
[41](https://fintech.theodo.com/blog-posts/tips-for-automating-your-github-release-creation)
[42](https://www.reddit.com/r/ClaudeCode/comments/1odoo3k/i_built_a_context_management_plugin_and_it/)
[43](https://github.com/release-it/release-it/issues/807)
[44](https://docs.ckan.org/en/2.11/changelog.html)
[45](https://maven.apache.org/plugins/maven-changelog-plugin/)
[46](https://nx.dev/docs/guides/nx-release/customize-conventional-commit-types)
[47](http://stackoverflow.com/questions/29832653/how-to-make-maven-changelog-plugin-generate-both-a-changelog-html-and-a-changel?rq=1)
[48](https://raw.githubusercontent.com/release-it/release-it/master/CHANGELOG.md)
[49](https://dev.to/rahulbanerjee99/how-to-package-existing-typescript-project-and-release-it-to-npm-in-5-steps-31d4)
[50](https://nextjs.org/docs/app/api-reference/config/typescript)
[51](https://blog.appsignal.com/2024/12/11/a-deep-dive-into-commonjs-and-es-modules-in-nodejs.html)
[52](https://devblogs.microsoft.com/typescript/announcing-typescript-5-9-rc/)
[53](https://plugins.jenkins.io/git-changelog)
[54](https://ruleoftech.com/2020/automate-versioning-and-changelog-with-release-it-on-gitlab-ci-cd)
[55](https://github.com/semantic-release/semantic-release/issues/952)
[56](https://semantic-release.gitbook.io/semantic-release/beta/developer-guide/plugin)
[57](https://docs.constructor.com/docs/integrating-with-constructor-connect-cli-cli-release-notes)
[58](https://turborepo.com/docs/guides/tools/typescript)
[59](https://docs.digital.ai/release/release-plugin-changelog)
[60](https://www.typescriptlang.org/tsconfig/)
[61](https://www.npmjs.com/package/release-it/v/2.8.5)
[62](https://docs.redhat.com/de/documentation/red_hat_build_of_node.js/22/html-single/release_notes_for_node.js_22/index)
[63](https://www.typescriptlang.org/docs/handbook/modules/theory.html)
[64](https://www.totaltypescript.com/books/total-typescript-essentials/configuring-typescript)
[65](https://github.com/git-lfs/git-lfs/issues/4210)
[66](https://github.com/release-it/release-it/issues/969)
[67](https://devblogs.microsoft.com/typescript/announcing-typescript-5-7-rc/)
[68](https://github.com/release-it-plugins/lerna-changelog)
[69](https://stackoverflow.com/questions/72457791/typescript-packages-that-ship-with-mjs-and-d-ts-but-without-d-mts-how-to-i)
[70](https://github.blog/changelog/)
[71](https://github.com/release-it/release-it/issues/859)
[72](https://github.com/release-it-plugins/workspaces)
[73](https://stackoverflow.com/questions/77097401/getting-recent-changes-for-generating-release-notes-on-github-enterprise)
[74](https://hackernoon.com/how-to-implement-semantic-release-for-public-non-scoped-packages)
[75](https://nodejs.org/en/learn/modules/publishing-a-package)
[76](https://docs.slack.dev/tools/slack-cli/reference/hooks/)
[77](https://github.com/release-it/release-it/issues/1186)
[78](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
[79](https://tyk.io/docs/5.0/context-variables/)
[80](https://stackoverflow.com/questions/70844794/conventional-github-releaser-doesnt-pick-up-changelog-md-as-github-release-desc)
[81](https://github.com/release-it/release-it/issues/1098)
[82](https://payloadcms.com/docs/hooks/context)
[83](https://legacy.reactjs.org/docs/hooks-reference.html)
[84](https://github.com/release-it/conventional-changelog/releases)
[85](https://github.com/release-it/release-it/issues/830)
[86](https://www.apollographql.com/docs/react/v3/api/react/hooks)
[87](https://github.com/conventional-changelog/conventional-changelog)
[88](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
[89](https://intuit.github.io/auto/docs/welcome/getting-started)
[90](https://github.com/release-it/release-it/issues/1163)
[91](https://github.com/release-it/release-it/issues/636)
[92](https://github.com/release-it/release-it/issues/662)
[93](https://github.com/release-it/release-it/issues/1136)
[94](https://github.com/release-it/release-it/issues/946)
[95](https://github.com/release-it/release-it/issues/801)
[96](https://github.com/release-it/release-it/issues/103)
[97](https://github.com/release-it/release-it/issues/551)
[98](https://github.com/release-it/release-it/issues/747)
[99](https://github.com/release-it/release-it/issues/501)
[100](https://stackoverflow.com/questions/72374197/how-to-show-changelog-alert-only-for-certain-app-versions)
[101](https://nx.dev/docs/guides/nx-release/configure-changelog-format)
[102](https://stackoverflow.com/questions/35115863/generate-changelog-for-a-semantically-released-package)
[103](https://stackoverflow.com/questions/68525678/standard-version-changelog-repeats-changes-in-different-releases)
[104](https://satya164.page/posts/automated-release-on-github-actions)
[105](https://codesandbox.io/examples/package/@release-it/conventional-changelog)
[106](https://stackoverflow.com/questions/71843736/how-to-automate-change-log-and-release-creation)
[107](https://www.conventionalcommits.org/en/about/)
[108](https://www.kodaps.dev/en/blog/how-to-push-your-code-into-the-wild-using-release-it)
[109](https://generalistprogrammer.com/tutorials/release-it-npm-package-guide)
[110](https://github.com/semantic-release/semantic-release/discussions/3158)
[111](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)
[112](https://stackoverflow.com/questions/77942972/is-possible-to-use-release-it-from-the-develop-branch)
[113](https://www.npmjs.com/package/release-it/v/13.5.5-changelog.0)
[114](https://stackoverflow.com/questions/36916989/how-can-i-generate-a-tsconfig-json-file)
[115](https://nodejs.org/download/release/v14.7.0/docs/api/esm.html)
[116](https://github.com/WebReflection/common-js)
[117](https://about.gitlab.com/blog/tutorial-automated-release-and-release-notes-with-gitlab/)
[118](https://github.com/configcat/common-js)
[119](https://www.mehdi-khalili.com/better-git-release-notes)
[120](https://dev.to/jakobjingleheimer/configuring-commonjs-es-modules-for-nodejs-12ed)
[121](https://drewdevault.com/2021/05/19/How-to-write-release-notes.html)
[122](https://docs.archivesspace.org/development/release/)
[123](https://github.com/configcat/common-js/releases)
[124](https://dev.to/github/how-to-automatically-generate-release-notes-for-your-project-2ng8)
[125](https://ull-esit-pl-2021.github.io/assets/temas/introduccion-a-javascript/nodejspackages.html)
[126](https://semantic-release.gitbook.io)
[127](https://release-it-pnpm.vercel.app)
[128](https://github.com/topics/commonjs)