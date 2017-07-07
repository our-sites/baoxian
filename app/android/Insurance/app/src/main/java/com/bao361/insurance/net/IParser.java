package com.bao361.insurance.net;

import org.json.JSONObject;

public interface IParser<T> {

    T parse(JSONObject result) throws Exception;
}
