package com.common.insurance.base;

import android.os.Handler;

import com.common.insurance.request.RequestHandler;

public abstract class AbsBusinessPresenter<V extends IBusinessView> implements IPresenter {

    protected V mView;
    protected Handler mRequestHandler = new PresenterRequestHandler();

    public AbsBusinessPresenter() {
    }

    public void setView(V view) {
        mView = view;
    }

    private static class PresenterRequestHandler extends RequestHandler {


        public PresenterRequestHandler() {
        }

        @Override
        protected void onSuccess(int what, Object response) {
            onSuccess(what, response);
        }

        @Override
        protected void onFail(int what, Object error) {

            onFail(what, error);
        }
    }

    protected void onSuccess(int what, Object response) {
    }

    protected void onFail(int what, Object error) {
    }

}
