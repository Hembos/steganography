# Стеганография
Проект для LSB стеганографии изображений, аудио файлов и видео

## Задания для стеганографии
Задания для стеганографии задаются в [config.xml](config.xml) файле

### Структура [config.xml](config.xml)
```xml
<works>
    <work>
        <type>ENCODE</type> <!-- Зашифровать или расшифровать данные: ENCODE, DECODE -->
        <file_type>AUDIO</file_type> <!-- Тип данных, в которые нужно зашивровать сообщение: AUDIO, VIDEO, IMAGE -->
        <inFile>data/msg1.txt</inFile> <!-- Путь к файлу с сообщением для шифрования -->
        <toFile>data/1.wav</toFile> <!-- Куда нужно зашифровать данные -->
        <outFile>data/out.wav</outFile> <!-- Выходной файл -->
    </work>

    <work>
        <type>DECODE</type>
        <file_type>AUDIO</file_type>
        <inFile>data/out.wav</inFile> <!-- Путь к файлу с зашифрованным сообщением -->
        <toFile></toFile>
        <outFile>data/decoded_msg1.txt</outFile>
    </work>
</works>
```
