package com.common.insurance.activity;

import android.os.Bundle;
import android.os.Message;
import android.view.View;

import com.common.insurance.R;
import com.common.insurance.request.BaseBusinessRequest;
import com.common.insurance.request.TestRequest;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends BaseActivity implements View.OnClickListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findViewById(R.id.fengzhuangpost).setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.fengzhuangpost:
                sendEncapsulationPost();
                break;
        }

    }

    private void sendEncapsulationPost() {

        Message message = mRequestHandler.obtainMessage();

        Map<String, String> map = new HashMap<>();
//        map.put("ip", "58.215.185.154");
//        map.put("dtype", "json");
//        map.put("key", "177038539bb5e9c91c8a1443145d3765");
        BaseBusinessRequest request = new TestRequest(this, map, message);
        request.execute();


    }

    @Override
    protected void onSuccess(int what, Object response) {
        super.onSuccess(what, response);
    }

    @Override
    protected void onFail(int what, Object error) {
        super.onFail(what, error);
    }
}
