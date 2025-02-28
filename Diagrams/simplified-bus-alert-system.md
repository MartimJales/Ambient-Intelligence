```mermaid
flowchart TD
    %% Core Components Only
    A[Bus] -->|Displays bus number| B[Station Camera]
    B -->|Captures image| C[Image Processing Server]
    C -->|Extracts bus number via OCR| D[Central Server]

    E[Bus GPS Transmitter] -->|Location data| D

    F[Alert Generator]
    F -->|When bus arrived| G[Station Audio System]
    G -->|Announces bus arrival| H[Blind Person at Station]

    %% Simple Decision Flow
    D -->|"If: Bus arrived + Number confirmed"| F

    style A fill:#3498DB,stroke:#2980B9,color:#FFF
    style C fill:#2ECC71,stroke:#27AE60,color:#FFF
    style D fill:#9B59B6,stroke:#8E44AD,color:#FFF
    style G fill:#F1C40F,stroke:#F39C12,color:#000
    style H fill:#E74C3C,stroke:#C0392B,color:#FFF
