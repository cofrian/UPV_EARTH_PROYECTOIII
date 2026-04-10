# Guia SSH y VS Code para abrir el repo

Esta guia explica como conectarse por SSH a una maquina Linux desde Visual Studio Code y como abrir la carpeta del repositorio en remoto.

## 1) Requisitos

- Tener una cuenta valida en la maquina remota.
- Tener instalado Visual Studio Code en tu equipo local.
- Instalar la extension Remote - SSH (Microsoft) en VS Code.
- Conocer estos datos:
  - Usuario SSH (ejemplo: `root` o `usuario`).
  - IP o hostname del servidor (ejemplo: `192.168.1.50` o `mi-servidor`).
  - Puerto SSH (normalmente `22`).

## 2) Configurar SSH en tu equipo local

Edita (o crea) el archivo `~/.ssh/config` en tu equipo local y agrega un bloque como este:

```ssh-config
Host upv-maquina
    HostName TU_IP_O_HOST
    User TU_USUARIO
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

Notas:

- Si usas otra clave, cambia `IdentityFile`.
- Si entras con password, puedes omitir `IdentityFile`.

## 3) Conectarte desde VS Code

1. Abre VS Code en tu equipo local.
2. Pulsa `F1` (o `Ctrl+Shift+P`).
3. Ejecuta el comando `Remote-SSH: Connect to Host...`.
4. Elige el host configurado (ejemplo: `upv-maquina`).
5. Acepta la huella del servidor si aparece.
6. Introduce password o passphrase de la clave cuando se solicite.

Cuando conecte bien, VS Code mostrara una ventana remota (SSH) con barra verde en la parte inferior.

## 4) Ir a la carpeta del repositorio remoto

Con la sesion SSH abierta en VS Code:

1. Pulsa `F1`.
2. Ejecuta `File: Open Folder...`.
3. Escribe o selecciona la ruta del repo:

```text
/root/proyectoiii
```

4. Confirma con `OK`.

Listo: ya estas trabajando directamente sobre la carpeta remota.

## 5) Verificar en terminal integrado

Abre una terminal en VS Code (`Terminal > New Terminal`) y ejecuta:

```bash
pwd
ls -la
git status
git remote -v
```

Debes ver que estas dentro de `/root/proyectoiii` y que el remoto apunta a GitHub.

## 6) Si el repo no existe en la maquina remota

Si aun no tienes la carpeta en el servidor, clona el repo asi:

```bash
cd /root
git clone https://github.com/cofrian/UPV_EARTH_PROYECTOIII.git proyectoiii
cd /root/proyectoiii
```

Luego abre esa misma ruta en VS Code remoto.

## 7) Problemas comunes

- Error `Permission denied (publickey)`:
  - Revisa usuario, clave privada y permisos en `~/.ssh`.
- Error `Connection timed out`:
  - Verifica IP, puerto y firewall.
- VS Code conecta pero no abre carpeta:
  - Revisa permisos de la ruta en el servidor (`/root/proyectoiii`).
- Git pide credenciales al hacer push:
  - Usa un token personal de GitHub con permisos al repo.

## 8) Flujo recomendado para nuevos usuarios

1. Configurar `~/.ssh/config`.
2. Conectar con `Remote-SSH: Connect to Host...`.
3. Abrir carpeta `/root/proyectoiii`.
4. Validar con `git status`.
5. Trabajar normalmente (editar, commit, push).