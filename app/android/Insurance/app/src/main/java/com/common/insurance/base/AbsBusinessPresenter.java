package com.common.insurance.base;



public abstract class AbsBusinessPresenter<V extends IBusinessView> implements IPresenter {

    protected V mView;

    public AbsBusinessPresenter() {
    }

    public void setView(V view) {
        mView = view;
    }





    protected void onSuccess(int what, Object response) {
    }

    protected void onFail(int what, Object error) {
    }

}
