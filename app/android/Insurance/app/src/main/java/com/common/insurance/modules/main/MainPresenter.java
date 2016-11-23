package com.common.insurance.modules.main;

import android.os.Message;

import com.common.insurance.base.AbsBusinessPresenter;
import com.common.insurance.request.BaseBusinessRequest;
import com.common.insurance.request.TestRequest;

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

        Message message = mRequestHandler.obtainMessage();
        Map<String, String> map = new HashMap<>();
        map.put("ip", "58.215.185.154");
        map.put("dtype", "json");
        map.put("key", "177038539bb5e9c91c8a1443145d3765");
        BaseBusinessRequest request = new TestRequest(map, message);
        request.execute();

    }
}
