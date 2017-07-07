package com.bao361.insurance.modules.main;

import com.bao361.insurance.base.AbsBusinessPresenter;
import com.bao361.insurance.model.WeatherInfo;
import com.bao361.insurance.net.RequestError;
import com.bao361.insurance.request.BaseBusinessRequest;
import com.bao361.insurance.request.LoadCallback;
import com.bao361.insurance.request.TestRequest;

import java.util.HashMap;
import java.util.Map;

public class MainPresenter extends AbsBusinessPresenter<MainView> {

    public MainPresenter() {
    }

    @Override
    protected void onSuccess(int what, Object response) {
        super.onSuccess(what, response);
        mView.setLoadingIndicator(false);
        mView.refresh();

    }

    @Override
    protected void onFail(int what, Object error) {
        super.onFail(what, error);
        mView.setLoadingIndicator(false);

    }

    public void sendEncapsulationPost() {
        mView.setLoadingIndicator(true);

        Map<String, String> map = new HashMap<>();
        map.put("ip", "58.215.185.154");
        map.put("dtype", "json");
        map.put("key", "177038539bb5e9c91c8a1443145d3765");
        //// TODO: 16/12/20 将来换成rxjava
        BaseBusinessRequest request = new TestRequest(map, new LoadCallback<WeatherInfo>() {
            @Override
            public void onLoadSuccess(WeatherInfo weatherInfo) {

            }

            @Override
            public void onLoadFail(RequestError error) {


            }
        });
        request.execute();

    }
}
