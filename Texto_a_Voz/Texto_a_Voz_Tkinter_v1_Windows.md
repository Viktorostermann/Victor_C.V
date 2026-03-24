# Texto_a_Voz_TkInter_v1 — Distribución para Windows

**Branding:** Viktore@ConquerBlocks — Software verificable

---

## ¿Qué hace este software?

Aplicación con interfaz gráfica (Tkinter) que permite:

* Convertir texto manual a audio
* Extraer texto desde páginas web
* Generar archivos de voz automáticamente
* Mantener registro del contenido procesado

### Funciones principales

* **Entrada:** texto manual o URL de artículo
* **Salida:** audio generado automáticamente
* **Registros:** historial de procesamiento
* **Interfaz:** entorno gráfico simple y directo

Los datos del usuario se almacenan automáticamente en:

```
%APPDATA%\Texto_a_Voz_TkInter_v1\
```

Allí encontrarás:

* Audios generados
* Registros de ejecución
* Reportes del programa

---

## Requisitos del sistema

* Windows 10 u 11 (64 bits)
* 4 GB RAM recomendados
* Conexión a Internet (solo para leer páginas web)
* Altavoces o auriculares

No es necesario instalar Python.

---

## Verificación de autenticidad

El programa puede verificarse:

1. Clic derecho sobre `Texto_a_Voz_TkInter_v1_Setup.exe`
2. Propiedades
3. Pestaña **Firmas digitales**

Si la firma aparece válida, el archivo no ha sido modificado.

---

## Instalación

1. Ejecutar:

```
Texto_a_Voz_TkInter_v1_Setup.exe
```

2. Seguir el asistente.
3. El programa se instalará en:

```
C:\Program Files\Texto_a_Voz_TkInter_v1\
```

Durante la instalación se creará:

* Acceso directo en el menú inicio
* (Opcional) acceso directo en escritorio
* Registro de desinstalación en Windows

---

## Ejecución

Abrir desde:

**Menú Inicio → Texto a Voz TkInter v1**

También puede ejecutarse directamente desde:

```
C:\Program Files\Texto_a_Voz_TkInter_v1\
```

---

## Desinstalación

Hay dos formas:

### Método recomendado

```
Configuración → Aplicaciones → Texto a Voz TkInter v1 → Desinstalar
```

### Limpieza completa opcional

Después de desinstalar, si deseas eliminar los datos guardados:

1. Presiona `Win + R`
2. Escribe:

```
%APPDATA%
```

3. Borra la carpeta:

```
Texto_a_Voz_TkInter_v1
```

---

## Solución de problemas

### El programa no abre

Ejecutar como Administrador la primera vez.

### Windows bloquea el archivo

Clic derecho → Propiedades → marcar **Desbloquear** → Aplicar.

### No se genera audio

* Verifica conexión a Internet
* Revisa la carpeta:

```
%APPDATA%\Texto_a_Voz_TkInter_v1\Logs_GUI
```

### No aparece el ícono

Reinicia el explorador de Windows o cierra sesión.

---

## Notas

* El programa no modifica archivos del sistema.
* Los audios pertenecen al usuario y no se eliminan automáticamente al desinstalar.
* El software funciona completamente offline para texto manual.

---

**Viktore@ConquerBlocks**
