```mermaid
flowchart TD
    subgraph BusSystem["Bus Onboard System"]
        BusGPS["GPS Transmitter"]
        BusID["Visual Identification System"]
    end

    subgraph StationSystem["Station System"]
        StationCamera["Recognition Camera"]
        AudioSystem["Audio System"]
        StationBeacon["Location Beacon"]
    end

    subgraph CentralSystem["Central System"]
        ImageServer["Image Processing Server"]
        CentralServer["Central Server"]
        AlertManager["Alert Manager"]
        RouteDB["Route Database"]
    end

    subgraph UserInterface["User Interface"]
        MobileApp["Mobile App"]
    end

    %% Connections between components
    BusGPS -->|"GPS Data"| CentralServer
    BusID -->|"Visible Number"| StationCamera
    StationCamera -->|"Images"| ImageServer
    ImageServer -->|"Identified Bus Number"| CentralServer
    StationBeacon -->|"Station ID"| CentralServer
    CentralServer -->|"Route Data"| RouteDB
    CentralServer -->|"Alert Command"| AlertManager
    AlertManager -->|"Audio Message"| AudioSystem
    AlertManager -->|"Notification"| MobileApp
    AudioSystem -->|"Sound Announcement"| User["Blind User at Station"]

    style BusSystem fill:#d4f1f9,stroke:#75b1c9
    style StationSystem fill:#d5f5e3,stroke:#82c4a3
    style CentralSystem fill:#e8daef,stroke:#b691b5
    style UserInterface fill:#fcf3cf,stroke:#d7c694
    style User fill:#f9d5e5,stroke:#c6a3b4
