# FastAPI mit Docker - Tutorial Nummer 2

Dieses Projekt zeigt einen FastAPI Server welcher in der Lage ist eine Textdatei entgegenzunehmen und diese in einer
Datei namens `temporary.txt` innerhalb des Docker-Containers abzulegen.

Im Anschluss wird die Datei geöffnet und ihr Inhalt zurückgegeben.

Es wird der `HTTP/POST`-Befehl genutzt. 

Der Server kann als Docker-Image gebaut werden, genau wie in Tutorial Nummer 1 zu FastAPI in Docker.
Nach dem Starten des Servers kann ein einfacher Test mit Hilfe von `cURL` erfolgen, indem man den folgenden Befehl nutzt:
```curl -X POST 127.0.0.1:80/upload -i -F "file=@.\test.txt"```
Selbstverständlich kann auch eine andere `.txt`-Datei genutzt werden. 
Es ist aber immer auf das `@` vor dem Dateipfad zu achten. 

`/upload` matcht dabei dem Endpoint-Namen innerhalb der Datei `./app/main.py`

