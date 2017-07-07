package com.bao361.insurance.base;

import android.os.Bundle;

public abstract class BaseMvpActivity<P extends AbsBusinessPresenter> extends BaseActivity implements IBusinessView {


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
