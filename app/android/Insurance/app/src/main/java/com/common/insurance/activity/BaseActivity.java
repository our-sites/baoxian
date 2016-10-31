package com.common.insurance.activity;

import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.FragmentActivity;

import com.common.insurance.request.RequestHandler;

import java.lang.ref.WeakReference;

public abstract class BaseActivity extends FragmentActivity {

    protected Handler mRequestHandler = new ActivityRequestHandler(this);


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }

    private static class ActivityRequestHandler extends RequestHandler {

        private WeakReference<BaseActivity> weakActivity;

        public ActivityRequestHandler(BaseActivity activity) {
            weakActivity = new WeakReference<BaseActivity>(activity);
        }

        @Override
        protected void onSuccess(int what, Object response) {

            if (weakActivity.get() == null || weakActivity.get().isFinishing()) {
                return;
            }

            weakActivity.get().onSuccess(what, response);
        }

        @Override
        protected void onFail(int what, Object error) {

            if (weakActivity.get() == null || weakActivity.get().isFinishing()) {
                return;
            }

            weakActivity.get().onFail(what, error);
        }
    }

    protected void onSuccess(int what, Object response) {
    }

    protected void onFail(int what, Object error) {
    }


}
