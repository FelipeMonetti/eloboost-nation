package com.eloboost.ggwp.model;

public class Booster {
    
    // Estos son los datos que va a tener cada booster
    private String id;          // Un identificador único (ej: 1, 2, 3)
    private String nickname;    // El nombre ficticio (ej: "FakerFan")
    private String rango;       // Ej: "Grandmaster 500LP"
    private String carril;      // Ej: "MID / JUNGLE"
    private String nacionalidad;// Ej: "ARG / CHI"
    private String champPool;   // Ej: "Zed, Yasuo, Yone"
    private String descripcion; // Texto vendedor
    private String fotoUrl;     // Link a la imagen del booster

    // Constructor Vacío (Spring lo necesita a veces)
    public Booster() {}

    // Constructor completo (Para crear boosters rápido)
    public Booster(String id, String nickname, String rango, String carril, String nacionalidad, String champPool, String descripcion, String fotoUrl) {
        this.id = id;
        this.nickname = nickname;
        this.rango = rango;
        this.carril = carril;
        this.nacionalidad = nacionalidad;
        this.champPool = champPool;
        this.descripcion = descripcion;
        this.fotoUrl = fotoUrl;
    }

    // Getters y Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getNickname() { return nickname; }
    public void setNickname(String nickname) { this.nickname = nickname; }

    public String getRango() { return rango; }
    public void setRango(String rango) { this.rango = rango; }

    public String getCarril() { return carril; }
    public void setCarril(String carril) { this.carril = carril; }

    public String getNacionalidad() { return nacionalidad; }
    public void setNacionalidad(String nacionalidad) { this.nacionalidad = nacionalidad; }

    public String getChampPool() { return champPool; }
    public void setChampPool(String champPool) { this.champPool = champPool; }

    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }

    public String getFotoUrl() { return fotoUrl; }
    public void setFotoUrl(String fotoUrl) { this.fotoUrl = fotoUrl; }
}