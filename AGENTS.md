# Producto Core: instrucciones para agentes

## Reglas propias de este repositorio (público, AGPL-3.0-only)

- **Nunca añadas `Signed-off-by`.** El DCO es una certificación que solo hace una persona; Jorge (u otro humano) firma tras revisar (`git rebase --signoff`). El check `dco` fallará en tus PR hasta entonces: es lo esperado, no lo «arregles» firmando tú.
- Cabeceras SPDX en todo archivo de código nuevo (`SPDX-FileCopyrightText` + `SPDX-License-Identifier: AGPL-3.0-only`). No toques `LICENSE`.
- Repositorio público: nada de datos de la empresa, clientes, rutas locales ni referencias a repos privados.
- Antes del PR: `python3 scripts/check_compliance.py` y `python3 -m unittest discover -s tests -v`.
- El flujo de release (`release.yml`) no se ejecuta ni se modifica sin petición explícita; nunca publiques releases ni etiquetas.

<!-- erlen-convencion-agentes:inicio v2 (bloque común; fuente: erlen-suite/docs/convencion.md; se actualiza en todos los repos a la vez) -->
## Trabajo con varios agentes

Este repositorio lo trabajan varios agentes (Claude, Codex, Amp, Mimo, Antigravity, Oh my Pi, Vibe) y modelos. Estas reglas son comunes a todos los repos de Erlen y prevalecen sobre costumbres de cada herramienta o instrucciones locales anteriores.

- **Nunca en `main`.** Trabaja en una rama `<agente>/<tarea-corta>` en minúsculas y con guiones (por ejemplo `codex/fix-export-csv`). Solo los bots usan otros prefijos: `diseno/` (paquete de diseño) y `sync/` (sincronización de la suite). `main` está protegida: todo entra por pull request y se fusiona con *squash*; la rama se borra al fusionar.
- **Una carpeta por agente y tarea.** Usa tu propio clon o worktree; no edites la carpeta de trabajo de otro agente ni la de Jorge.
- **No fusiones ni apruebes.** Abre el PR y detente; Jorge revisa y fusiona. Si otro PR abierto toca los mismos archivos, dilo en tu PR en lugar de pisarlo.
- **Cambios que cruzan repos.** Si tu cambio afecta a otra app o a la suite (paquete de diseño, módulos compartidos `suite-*.mjs`/`mey.mjs`, formatos de intercambio, avisos a la suite), usa **el mismo nombre de rama en cada repo afectado** y enlaza todos los PRs en la sección *Cross-repo*. Se fusionan juntos: primero `erlen-suite`, después las apps. No copies módulos compartidos a mano: vienen de `erlen-suite` por `diseno-propagar`.
- **CI intocable sin permiso.** No modifiques `.github/` salvo petición explícita en la tarea.
- **Commits y títulos de PR** en inglés con Conventional Commits (`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`; ámbito opcional en minúsculas), sin tildes ni eñes en el título. El título del PR se convierte en el commit de `main` y lo valida el check `convencion`. Identifica agente y modelo con trailers (`Co-Authored-By` es opcional):
  ```
  Agent: codex
  Agent-Model: <modelo exacto>
  ```
- **Antes del PR** ejecuta las pruebas del repo y copia el resultado real en la descripción (sección *Testing* de la plantilla). No afirmes pruebas que no ejecutaste.
- **Nada sensible:** ni secretos, tokens, datos personales, contratos ni expedientes. Si encuentras uno, detente y avisa.
- Los repos `empresa-*`, `erlen-legal-mexico` y `erlen-burocracy` están fuera del alcance de los agentes.
<!-- erlen-convencion-agentes:fin -->
