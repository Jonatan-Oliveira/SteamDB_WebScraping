# SteamDB_WebScraping

Case:

Realize a extração das informações que conseguir da base de dados listada no website:

https://steamdb.info/sales/

Armazene estes dados no Google BigQuery
Em seguida exporte ou conecte esses dados em um Google Sheets e nos envie o link.
Atenção:

Você deve criar um repositório público e não listado em um GIT para compartilhar conosco;
Compartilhar o Sheets final (o link precisa ser público);
Lembrar de pôr no repositório os arquivos da automação;



Para este projeto, foram usados as seguintes tecnologias: 

- **Python**: Para criar desenvolvimento do webscraping;
- **Github para armazenamento dos arquivos;
- **Google Cloud Platform:** Para armazenamento de dados;
- **Big Query:** Para armazenamento de dados;
- **Google sheets;


Observações:

O site em questão implementou uma série de mecanismos para prevenir a extração não autorizada de dados, conhecida como raspagem de dados. Essas medidas incluem a utilização de cookies de proteção fornecidos pelo servidor Cloudflare. Além disso, o servidor também realiza verificações mais complexas, como a execução de scripts de validação em JavaScript, com o objetivo de dificultar ainda mais o processo de raspagem.

Tentei acesso via API, mas a pagina só oferece a mesma caso a pessoa tenha jogos na plataforma, caso não tenha não é possivel o acesso, testei via bibliotecas Python diretamente no site também sem sucesso.

Para contornar essas proteções, entrei na pagina https://steamdb.info/sales/ e apenas salvei a pagina em formato HTML na minha maquina assim quebrando toda a segurança que existe na página, depois foi só fazer a manipulação diretamente do arquivo no script Python.