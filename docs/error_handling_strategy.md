# Estrategia de Manejo de Errores - regulon_summary.py

## Principio: Decisiones Justificadas, No Try/Except Indiscriminado

Este documento justifica EXPLÍCITAMENTE qué errores maneja el programa y cuáles no.

---

## 1. load_interactions(filename)

### ✓ MANEJA (Errors)
| Error | Por qué | Acción |
|-------|--------|--------|
| `FileNotFoundError` | Usuario proporciona ruta inválida | `RuntimeError` + exit |
| `PermissionError` | Permisos insuficientes del SO | `RuntimeError` + exit |
| `UnicodeDecodeError` | Encoding inválido (no UTF-8) | `RuntimeError` + exit |
| `OSError` | I/O inesperado del sistema | `RuntimeError` + exit |
| Archivo vacío | Sin datos, no hay procesamiento válido | `RuntimeError` + exit |
| Líneas mal formadas | < 6 campos | Advertencia + skip (recuperable) |
| Campos vacíos | TF o gene sin contenido | Advertencia + skip (recuperable) |
| Effect inválido | Ni "+" ni "-" | Advertencia + skip (recuperable) |

### ✗ NO MANEJA
| Error | Por qué |
|-------|--------|
| `IndexError` | Si ocurre = bug en validación de campos → debe fallar visiblemente |
| `ValueError` | Si ocurre en conversiones = bug lógico → debe fallar visiblemente |
| `MemoryError` | Problema del sistema, no recuperable |

### Patrón: Validación Explícita Primero
```python
# ANTES del try/except (sin captura):
if not os.path.exists(filename):
    raise RuntimeError(...)  # Fail fast

# DENTRO del try/except (solo I/O):
with open(filename) as f:
    # procesamiento
```

---

## 2. build_regulon(interactions)

### ✓ MANEJA
**Nada** - No tiene try/except. Es una función pura que agrupa datos.

### ✗ NO MANEJA
| Error | Por qué |
|-------|--------|
| `KeyError`, `TypeError` | Si ocurren = bug en entrada de datos → debe fallar visiblemente |

**Justificación**: Si `interactions` tiene formato incorrecto, es un bug en `load_interactions()`, no del usuario.

---

## 3. write_regulon_summary(regulon, output_file)

### ✓ MANEJA
| Error | Por qué | Acción |
|-------|--------|--------|
| `PermissionError` | Permisos insuficientes para escribir | `RuntimeError` + exit |
| `OSError` | I/O inesperado del sistema | `RuntimeError` + exit |

### ✗ NO MANEJA
| Error | Por qué |
|-------|--------|
| `KeyError`, `TypeError` | Si ocurren en acceso a `regulon` = bug en `build_regulon()` |
| `UnicodeError` | Improbable en escritura UTF-8, indica bug del sistema |

**Justificación**: Solo capturamos problemas I/O predecibles; lógica de datos son responsabilidad de funciones previas.

---

## 4. parse_arguments()

### ✓ MANEJA
**Nada** - argparse ya valida automáticamente:
- Argumentos faltantes → SystemExit (argparse)
- Tipo incorrecto (--min_genes "abc") → SystemExit (argparse)

**Validación explícita** (sin try/except):
```python
if args.min_genes < 1:
    parser.error(...)  # Fail fast
```

### ✗ NO MANEJA
Cualquier error en argparse es fatal → no capturamos.

---

## 5. main()

### ✓ MANEJA
| Error | Por qué | Acción |
|-------|--------|--------|
| `RuntimeError` | De load_interactions() o write_regulon_summary() | Imprime + exit |

### ✗ NO MANEJA
| Error | Por qué |
|-------|--------|
| `KeyError`, `TypeError` | Bug de lógica en pipeline |
| `OSError` al crear directorios | Capturado antes del try/except |
| ArgumentParser errors | Ya abortados por argparse |

**Justificación**: Solo capturamos `RuntimeError` porque son los únicos errores *esperados y recuperables* del pipeline.

---

## Matriz de Decisión

```
ERROR OCURRE        ¿Es predecible?    ¿Usuario puede arreglarlo?    ACCIÓN
─────────────────────────────────────────────────────────────────────────
Archivo no existe   ✓ (FileNotFoundError) ✓ (proporcionar ruta)      CAPTURAR → RuntimeError
Permisos OS         ✓ (PermissionError)   ✓ (cambiar permisos)      CAPTURAR → RuntimeError
Línea mal formada   ✓ (validación)        ✓ (arreglar datos)        CAPTURAR → Advertencia + skip
Encoding inválido   ✓ (UnicodeDecodeError)✓ (usar UTF-8)           CAPTURAR → RuntimeError
─────────────────────────────────────────────────────────────────────────
IndexError          ✗ (bug código)        ✗ (bug del programa)      NO CAPTURAR → stack trace
KeyError            ✗ (bug lógica)        ✗ (bug del programa)      NO CAPTURAR → stack trace
MemoryError         ✗ (sistema)           ✗ (fuera de alcance)      NO CAPTURAR → stack trace
```

---

## Beneficios de Esta Estrategia

1. **Transparencia**: Cada try/except tiene justificación documentada
2. **Depuración fácil**: Bugs de lógica fallan con stack trace completo (no silenciados)
3. **UX clara**: El usuario ve:
   - Errores predecibles con mensaje específico
   - Bugs del programa con traceback completo
4. **Mantenibilidad**: Nuevos desarrolladores entienden la intención de cada bloque try/except
5. **No indiscriminado**: No capturamos `Exception` genéricamente; específico y justificado

---

## Checklist de Cumplimiento

- [x] Cada try/except tiene documentación explícita
- [x] Validaciones explícitas ANTES de try/except (no dentro)
- [x] Errores predecibles → capturados y convertidos a RuntimeError
- [x] Bugs de lógica → NO capturados (stack trace visible)
- [x] Errores I/O → capturados (PermissionError, OSError)
- [x] Advertencias no-fatales → print + continue (no exit)
