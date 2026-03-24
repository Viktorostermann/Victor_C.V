# Texto_a_Voz_TkInter_v1 — Distribución verificada

> Branding: Viktore@ConquerBlocks — Paquete firmado y verificable

## Índice

1. [¿Qué hace este software? Objetivo](#que-hace-este-software-objetivo)
2. [Requisitos previos](#requisitos-previos)
3. [Verificar autenticidad de la distribución](#verificar-autenticidad-de-la-distribucion)
4. [Instalación](#instalacion)
   4.1. [Instalar desde paquete .deb](#41-instalar-desde-paquete-deb)  
   4.2. [Instalación remota con script](#42-instalacion-remota-con-script)
5. [Desinstalación](#desinstalacion)
6. [Uso de scripts .sh](#uso-de-scripts-sh)
   6.1. [instalar_remoto.sh](#61-instalar_remotosh)  
   6.2. [desinstalar.sh](#62-desinstalarsh)
7. [Ejecución y lanzador](#ejecucion-y-lanzador)
8. [Solución de problemas](#solucion-de-problemas)

---

## ¿Qué hace este software? Objetivo

**Objetivo:** Proveer una interfaz gráfica en Tkinter para convertir texto (incluyendo texto extraído de la web) a audio, guardando reportes y manteniendo trazabilidad del contenido.

**Funciones clave:**
- **Entrada:** texto manual o fuentes web compatibles.
- **Salida:** archivos de audio en Reportes/Audios_URLS/ y registros en Reportes/Logs_GUI/.
- **Experiencia visual:** ícono e identidad de marca en el lanzador y en recursos.
- **Trazabilidad:** estructura de reportes organizada y verificable.

---

## Requisitos previos

- **Sistema:** Distribuciones basadas en Debian/Ubuntu.
- **Dependencias del sistema (audio):**
  - libasound2, libglib2.0-0, libgomp1 (según entorno).
- **GPG:** para verificación de firma digital.

> Tip: Si falta alguna librería, el instalador .deb intentará resolverlas automáticamente vía apt.

---

## Verificar autenticidad de la distribución

Antes de instalar, verifica la firma del paquete.

1. **Importa la clave pública:**
   ```bash
   gpg --import viktore_public.asc


Verifica la firma del .deb:

bash
gpg --verify Texto_a_Voz_TkInter_v1_DEB.deb.sig Texto_a_Voz_TkInter_v1_DEB.deb
Resultado esperado: “Firma correcta de Viktore <viktore@conquerblocks.local>”. Si el mensaje es correcto, el paquete es auténtico y no ha sido modificado.

Instalación
4.1. Instalar desde paquete .deb
Instala el paquete:

bash
sudo dpkg -i Texto_a_Voz_TkInter_v1_DEB.deb || sudo apt -f install -y
Verifica archivos instalados (opcional):

Binario: /usr/local/bin/Texto_a_Voz_TkInter_v1

App: /opt/Texto_a_Voz_TkInter_v1/

Ícono: /usr/share/icons/nouki.png

Lanzador: /usr/share/applications/Texto_a_Voz_TkInter_v1.desktop

4.2. Instalación remota con script
Dar permisos de ejecución al script (si aplica):

bash
chmod +x instalar_remoto.sh
Ejecutar el script:

bash
./instalar_remoto.sh
Qué hace: valida el .deb, instala dependencias faltantes, registra el lanzador e ícono.

Desinstalación
Opción A — Script de desinstalación:

bash
chmod +x desinstalar.sh
./desinstalar.sh
Opción B — dpkg/apt:

bash
sudo dpkg -r texto-a-voz-tkinter-v1 || sudo apt remove -y texto-a-voz-tkinter-v1
El nombre del paquete puede variar según el control del .deb. Ajusta si usaste otro nombre en DEBIAN/control.

Uso de scripts .sh
6.1. instalar_remoto.sh
Propósito: Automatizar verificación e instalación.

Uso:

bash
./instalar_remoto.sh
Acciones típicas:

Verificación: gpg --verify del .deb y .sig con viktore_public.asc.

Instalación: dpkg -i y apt -f install para dependencias.

6.2. desinstalar.sh
Propósito: Quitar el paquete y limpiar recursos.

Uso:

bash
./desinstalar.sh
Acciones típicas:

Remoción: dpkg -r del paquete.

Limpieza: opcional de /opt/Texto_a_Voz_TkInter_v1/ y reportes si el usuario lo elige.

Ejecución y lanzador
Desde terminal:

bash
Texto_a_Voz_TkInter_v1
Desde interfaz gráfica: Busca “Texto a Voz (Tkinter)” en el menú de aplicaciones. El lanzador apunta al binario e incluye ícono de marca.


Solución de problemas

Firma inválida: Repite la importación de la clave y verifica la fecha de los archivos.

Dependencias faltantes: Ejecuta sudo apt -f install -y tras dpkg -i.

Audio no suena: Verifica libasound2 e intenta desde terminal para ver logs.

Ícono no aparece: Refresca la caché de iconos o relanza la sesión; revisa que nouki.png esté en /usr/share/icons/.




