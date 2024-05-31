# Discord Migration Bot

La finalidad principal de este bot es facilitar la migración de mensajes o incluso servidores enteros en Discord.

Está organizado en una serie de comandos básicos para llevar a cabo estas migraciones:

- **Migración de Canal**:

    `!export_msg id_canal_origen id_servidor_destino id_canal_destino`

- **Migración de Servidor**:

    Para ejecutar este comando, primero necesitamos crear un servidor utilizando la plantilla del servidor existente. Esto se hace en Configuración del servidor > Plantilla del servidor. Luego, simplemente sigue los pasos proporcionados.

    `!full_backup id_servidor_destino`

- **Replicar canales, categorías y roles**:

    Este comando replica todos los canales, categorías y roles en un nuevo servidor. Se aconseja ejecutarlo en un servidor sin contenido previo..

    `!clone_server_to_blank_server id_servidor_destino`

- **Información del servidor**:

    Este comando presenta una lista de categorías y canales, así como una lista separada de roles.

    `!server_info`

- **Guía de plantillas**:

    `!create_template_guide`

- **Cambio de idiomas**:

    Actualmente, hay dos idiomas agregados al bot: español e inglés. Las claves son las siguiente: 'es' corresponde a español y 'en' a inglés.

    `!set_bot_language lenguaje`

Para obtener las ID de servidores o canales, es necesario habilitar el modo de desarrollador. Esto permitirá hacer clic derecho en un canal o servidor para mostrar la opción de copiar la ID. Para activar el modo de desarrollador, simplemente ve a Configuración de usuario > Avanzado y actívalo allí.

---

The main purpose of this bot is to facilitate the migration of messages or even entire servers in Discord.

It is organized into a series of basic commands to carry out these migrations:

- **Channel Migration**:

    `!export_msg(source_channel_id, destination_server_id, destination_channel_id: int)`

- **Server Migration**:

    To execute this command, we first need to create a server using the template of the existing server. This is done in Server Settings > Server Template. Then, simply follow the steps provided.

    `!full_backup(current_server_id, destination_server_id)`

- **Replicate channels, categories, and roles**:

    This command replicates all channels, categories, and roles to a new server. It is advisable to run it on a server without previous content.

    `!clone_server_to_blank_server destination_server_id`

- **Server information**:

    This command presents a list of categories and channels, as well as a separate list of roles.

    `!server_info`

- **Template guide**:

    `!create_template_guide`

- **Language Change**:

    Currently, the bot supports two languages: Spanish and English. 'es' corresponds to Spanish, and 'en' to English.

    `!set_bot_language language`

To obtain the IDs of servers or channels, it is necessary to enable developer mode. This will allow right-clicking on a channel or server to display the option to copy the ID. To activate developer mode, simply go to User Settings > Advanced and enable it there.
