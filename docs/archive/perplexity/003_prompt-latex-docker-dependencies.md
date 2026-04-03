# Prompt para Investigación: Gestión de Dependencias LaTeX en Docker para Compilación Reproducible

## Contexto Completo del Proyecto

### Stack Tecnológico Actual (YA IMPLEMENTADO)

**NO estamos buscando cambiar el stack, solo resolver dependencias LaTeX:**

- **release-it** con **pnpm**: Ya configurado y funcionando
- **@release-it/bumper**: Sincroniza versiones en `package.json`, `CITATION.cff`, `.zenodo.json`
- **TypeScript + tsx**: Scripts modulares en `scripts/` (orchestrator, tasks, utils)
- **Docker para LaTeX**: Usando `nanozoo/pdflatex:3.14159265--f2f4a3f`
- **Zenodo webhook**: Integración automática (NO queremos Actions adicionales)
- **GitHub Releases**: Automatizados vía release-it

**Estructura actual:**
```
scripts/
├── build.ts              # Script independiente para build (sin release)
├── release-orchestrator.ts  # Solo stagea archivos (build ya hecho)
├── tasks/
│   ├── citation.ts       # Actualiza date-released en CITATION.cff
│   ├── compile.ts        # Compila PDF con Docker ← AQUÍ ESTÁ EL PROBLEMA
│   ├── checksums.ts      # Genera SHA256
│   └── git-stage.ts      # Stagea archivos para commit
└── utils/
    ├── git.ts
    ├── filesystem.ts
    └── exec.ts
```

**Flujo actual (funcionando):**
```
pnpm run build
  → Actualiza CITATION.cff date-released
  → Compila PDF con Docker (PROBLEMA: falta paquete)
  → Genera checksums.txt

pnpm run release
  → Ejecuta build
  → release-it actualiza versiones
  → Stagea archivos
  → Git commit + tag
  → GitHub Release
  → Zenodo webhook automático
```

### Restricciones Críticas (NO NEGOCIABLES)

1. **NO queremos Actions adicionales**: Solo lo indispensable. Ya tenemos release-it + Zenodo webhook.
2. **NO queremos cambiar release-it**: Ya está configurado y funcionando con pnpm.
3. **NO queremos cambiar la estructura de scripts**: TypeScript modular ya implementado.
4. **Minimalismo**: Preferimos soluciones simples y estándar sobre complejidad.
5. **Solo resolver dependencias LaTeX**: El problema es específico: falta `annotate-equations.sty` (y posiblemente otros) en la imagen Docker.

### Problema Específico

**Error actual:**
```
! LaTeX Error: File `annotate-equations.sty' not found.
```

**Contexto del error:**
- Imagen Docker: `nanozoo/pdflatex:3.14159265--f2f4a3f` (minimalista, date-tagged)
- Documento requiere paquetes personalizados y CTAN especializados
- Compilación funciona localmente (todos los paquetes instalados)
- En Docker falla por paquetes faltantes

**Código actual en `scripts/tasks/compile.ts`:**
```typescript
const DOCKER_IMAGE = 'nanozoo/pdflatex:3.14159265--f2f4a3f';

export function compilePDF(config: ReleaseConfig): void {
  const commitEpoch = getCommitEpoch();
  
  const dockerCmd = `docker run --rm \
    -v $(pwd):$(pwd) \
    -w $(pwd) \
    -e SOURCE_DATE_EPOCH=${commitEpoch} \
    -e LC_ALL=C \
    -e LANG=C \
    -e TZ=UTC \
    ${DOCKER_IMAGE} \
    pdflatex -interaction=nonstopmode -output-directory=build main.tex`;
  
  execSync(dockerCmd, { stdio: 'inherit' });
  // ... resto del código
}
```

### Requisitos de la Solución

1. **Integración con código existente**: Debe funcionar dentro de `scripts/tasks/compile.ts`
2. **Reproducibilidad**: Mismo commit = mismo PDF (bit-a-bit)
3. **Determinismo**: SOURCE_DATE_EPOCH, primitives de LaTeX ya implementados
4. **Simplicidad**: Preferimos herramientas existentes sobre scripts custom
5. **Mantenibilidad**: Solución estándar, bien documentada
6. **Performance**: No agregar overhead significativo al build

### Lo que NO necesitamos

- ❌ Cambiar release-it o su configuración
- ❌ Agregar GitHub Actions (ya tenemos lo necesario)
- ❌ Cambiar estructura de scripts TypeScript
- ❌ Herramientas para gestión de versiones (ya resuelto)
- ❌ Herramientas para metadata Zenodo (ya resuelto)
- ❌ Soluciones para multi-idioma (v1 español, v2 inglés - no simultáneo)

### Lo que SÍ necesitamos

- ✅ Solución para instalar/verificar dependencias LaTeX en Docker
- ✅ Gestión de paquetes personalizados (`.sty`, `.cls` en el repo)
- ✅ Gestión de paquetes CTAN faltantes
- ✅ Integración elegante con el código TypeScript existente

## Preguntas de Investigación Específicas

### 1. Soluciones Estándar para Dependencias LaTeX en Docker

**Pregunta**: ¿Cómo resuelven otros proyectos científicos el problema de paquetes LaTeX faltantes en imágenes Docker minimalistas?

**Investigar:**
- Repositorios de papers en GitHub que usan Docker + LaTeX
- Patrones comunes: Dockerfile multi-stage, Makefile, scripts de instalación
- Herramientas que detectan dependencias faltantes automáticamente
- Best practices para paquetes personalizados vs CTAN

**Ejemplos de búsqueda:**
- GitHub: `latex docker dependencies` + `tlmgr install`
- GitHub: `reproducible latex` + `dockerfile`
- Repos que publican su pipeline de compilación

### 2. Herramientas Open Source Especializadas

**Pregunta**: ¿Existen herramientas open source bien mantenidas que resuelven específicamente dependencias LaTeX en Docker?

**Investigar:**
- Herramientas que parsean `.tex` y detectan `\usepackage` faltantes
- Herramientas que instalan automáticamente paquetes CTAN vía `tlmgr`
- Herramientas que gestionan paquetes personalizados (copiar `.sty`/`.cls` a `texmf-local`)
- Herramientas que generan Dockerfiles con dependencias correctas

**Criterios de evaluación:**
- ⭐ Stars en GitHub (>100 preferible)
- 📅 Última actualización reciente (<6 meses)
- 📚 Documentación completa
- 🔧 Mantenimiento activo
- 🎯 Enfoque específico en LaTeX

**Ejemplos de búsqueda:**
- GitHub: `latex-deps`, `tex-dependency-manager`, `latex-docker-helper`
- GitHub: `tlmgr` + `docker` + `dependencies`

### 3. Estrategias de Implementación

**Opciones a evaluar (en orden de preferencia):**

#### Opción A: Dockerfile Multi-stage con Instalación
```dockerfile
FROM nanozoo/pdflatex:3.14159265--f2f4a3f AS base
# Instalar paquetes CTAN faltantes
RUN tlmgr install annotate-equations <otros-paquetes>
# Copiar paquetes personalizados
COPY *.sty *.cls /usr/local/texlive/texmf-local/tex/latex/local/
RUN mktexlsr
```

**Preguntas:**
- ¿`tlmgr` está disponible en `nanozoo/pdflatex`?
- ¿Cómo detectar qué paquetes faltan automáticamente?
- ¿Cómo cachear la imagen con dependencias para builds rápidos?
- ¿Cómo integrar esto en el script TypeScript existente?

#### Opción B: Makefile con Verificación Pre-compilación
```makefile
.PHONY: check-deps install-deps
check-deps:
	@kpsewhich annotate-equations.sty >/dev/null || make install-deps

install-deps:
	docker run --rm -v $(pwd):/workdir nanozoo/pdflatex:... \
		tlmgr install annotate-equations
```

**Preguntas:**
- ¿Es estándar este patrón en la comunidad?
- ¿Cómo funciona en CI/CD (GitHub Actions)?
- ¿Ventajas/desventajas vs Dockerfile?

#### Opción C: Script TypeScript que Instala Dependencias
```typescript
// En scripts/tasks/compile.ts
function ensureDependencies() {
  // Detectar paquetes faltantes
  // Instalar vía tlmgr en Docker
  // Verificar instalación
}
```

**Preguntas:**
- ¿Existen librerías Node.js/TypeScript para esto?
- ¿Cómo detectar dependencias faltantes sin compilar?
- ¿Cómo parsear `\usepackage` del `.tex`?

#### Opción D: Herramienta Especializada (si existe)
- ¿Existe algo como `latex-deps` o `tex-dependency-manager`?
- ¿Herramientas que resuelven dependencias transitivas?
- ¿Herramientas que generan Dockerfiles automáticamente?

### 4. Gestión de Paquetes Personalizados

**Pregunta**: ¿Cómo gestionan otros proyectos los paquetes `.sty`/`.cls` personalizados que están en el repositorio?

**Investigar:**
- Patrones: copiar a `texmf-local`, usar `TEXINPUTS`, etc.
- Herramientas que gestionan paquetes personalizados
- Best practices para versionar paquetes personalizados
- Integración con Docker

**Contexto del proyecto:**
- Tenemos `lapreprint.cls` en el repo
- Posiblemente otros `.sty` personalizados
- Necesitan estar disponibles en Docker

### 5. Optimización y Caching

**Pregunta**: ¿Cómo optimizar builds considerando instalación de dependencias?

**Investigar:**
- Caching de imágenes Docker con dependencias pre-instaladas
- Estrategias de build incremental
- Trade-offs: imagen minimalista + instalación vs imagen completa

## Criterios de Evaluación

Para cada solución, evaluar:

1. **Simplicidad**: ¿Es fácil de entender e integrar en código existente?
2. **Estándar**: ¿Es un patrón común en la comunidad científica?
3. **Mantenibilidad**: ¿Requiere mantenimiento manual o es automático?
4. **Performance**: ¿Impacto en tiempo de compilación?
5. **Reproducibilidad**: ¿Garantiza builds determinísticos?
6. **Integración**: ¿Funciona bien con TypeScript/Node.js existente?

## Formato de Respuesta Esperado

### 1. Resumen Ejecutivo
- Solución recomendada (1-2 párrafos)
- Justificación breve
- **Cómo se integra con release-it y scripts TypeScript existentes**

### 2. Análisis de Herramientas Open Source
- Tabla comparativa de herramientas encontradas
- Evaluación según criterios
- Recomendación específica con justificación
- **Ejemplos de uso con TypeScript/Node.js**

### 3. Patrones Comunes en la Comunidad
- Ejemplos de repositorios que resuelven el problema
- Patrón más común identificado
- Variaciones del patrón
- **Links a repos de ejemplo**

### 4. Solución Recomendada Detallada
- **Código TypeScript de ejemplo** (modificando `scripts/tasks/compile.ts`)
- Arquitectura propuesta
- Pasos de implementación
- Consideraciones de CI/CD
- **Cómo mantener reproducibilidad**

### 5. Alternativas Evaluadas
- Otras soluciones consideradas
- Por qué no fueron seleccionadas
- Cuándo podrían ser apropiadas

### 6. Referencias y Recursos
- Links a repositorios de ejemplo
- Documentación relevante
- Herramientas mencionadas

## Información Adicional del Proyecto

- **Repositorio**: https://github.com/omega-pcf/01-primitive-complex-field
- **Tipo de documento**: Paper académico matemático (preprint)
- **Clase de documento**: `lapreprint.cls` (custom, en el repo)
- **Paquetes personalizados**: `.sty` y `.cls` en el repositorio
- **Paquetes CTAN**: Múltiples, algunos especializados (ej: `annotate-equations`)
- **CI/CD**: GitHub Actions (mínimo, solo lo indispensable)
- **Objetivo**: Compilación reproducible para releases automáticos en Zenodo
- **Versión actual**: v1.0.3 (español), próximo v2.0.0 (inglés)

## Prioridades

1. **Máxima prioridad**: Solución que se integre con código TypeScript existente sin cambiar release-it
2. **Alta prioridad**: Simplicidad y mantenibilidad
3. **Media prioridad**: Performance (pero no a costa de simplicidad)
4. **Baja prioridad**: Features avanzadas (si complican la solución)

## Restricciones Finales

**NO sugerir:**
- Cambiar release-it o su configuración
- Agregar GitHub Actions adicionales
- Cambiar estructura de scripts TypeScript
- Soluciones que requieran reescribir código existente

**SÍ sugerir:**
- Modificaciones mínimas a `scripts/tasks/compile.ts`
- Herramientas que se integren con el flujo existente
- Soluciones estándar y bien mantenidas
- Código de ejemplo específico para TypeScript

---

**Nota crítica**: Este proyecto YA tiene release-it funcionando, scripts TypeScript modulares, y un flujo de release automatizado. Solo necesitamos resolver el problema específico de dependencias LaTeX faltantes en Docker. Cualquier solución debe integrarse con el código existente, no reemplazarlo.
