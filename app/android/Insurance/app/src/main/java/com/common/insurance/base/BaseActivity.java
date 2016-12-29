package com.common.insurance.base;

import android.os.Bundle;
import android.support.v4.app.FragmentActivity;

public abstract class BaseActivity<P extends AbsBusinessPresenter> extends FragmentActivity implements IBusinessView {


    private P mPresenter;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mPresenter = createPresenter();
        mPresenter.setView(this);

    }

    protected abstract P createPresenter();

    public P getPresenter() {
        return this.mPresenter;
    }

}
