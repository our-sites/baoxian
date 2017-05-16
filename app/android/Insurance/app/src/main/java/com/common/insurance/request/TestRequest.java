package com.common.insurance.request;

import com.common.insurance.model.WeatherInfo;
import com.common.insurance.utils.InsuranceConstans;

import java.util.Map;

/**
 * Created by wangyongchao on 16/10/19.
 */
public class TestRequest extends BaseBusinessRequest<WeatherInfo> {


    public TestRequest(Map<String, String> params, LoadCallback callback) {
        super(params, callback);
    }

    @Override
    protected String createRequestHostPrefix() {
        return InsuranceConstans.TEST_WEATHER_URL;
    }

    @Override
    protected String createRequestHostPostfix() {
        return null;
    }

    @Override
    protected Class<WeatherInfo> getParseClass() {
        return WeatherInfo.class;
    }
}
