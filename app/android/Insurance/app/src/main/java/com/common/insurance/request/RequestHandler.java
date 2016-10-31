package com.common.insurance.request;


import android.os.Handler;
import android.os.Looper;
import android.os.Message;


public abstract class RequestHandler extends Handler {

    public RequestHandler() {
        super();
    }

    public RequestHandler(Looper looper) {
        super(looper);
    }

    @Override
    public void handleMessage(Message msg) {
        super.handleMessage(msg);

        if (msg.obj == null) {
            return;
        }

        // success
        int result = msg.arg1;
        if (result == 0) {

            // 处理响应内容
            onSuccess(msg.what, msg.obj);
        }

        // faill
        else if (result == 1) {
            onFail(msg.what, msg.obj);
        }
    }


    protected abstract void onSuccess(int what, Object response);


    protected abstract void onFail(int what, Object response);


}
