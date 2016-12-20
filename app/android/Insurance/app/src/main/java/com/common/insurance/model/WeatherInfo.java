package com.common.insurance.model;

import java.io.Serializable;

public class WeatherInfo implements Serializable {

    private SK sk;

    public void setSk(SK sk) {
        this.sk = sk;
    }

    public SK getSk() {
        return sk;
    }
}