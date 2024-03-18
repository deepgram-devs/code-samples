# Java

## Update the Code

Replace the placeholder code such as `DEEPGRAM_API_KEY` with your own information.

## Compile the Code

Compile the code in the `java` folder by running the following. You will see a `target` folder created with the compiled classes.

```
mvn compile
```

## Run the Files

Run the command `mvn exec:java -Dexec.mainClass="<PATH>.Main"`. Be sure to add each folder contained in the path after `java`.

For example, this runs the `Main.java` file within `java/prerecorded/local/httpURLConnection`:

```
mvn exec:java -Dexec.mainClass="prerecorded.local.httpURLConnection.Main"
```
