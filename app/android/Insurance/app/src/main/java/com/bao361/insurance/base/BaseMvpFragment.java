package com.bao361.insurance.base;

import android.os.Bundle;
import android.support.v4.app.Fragment;

public abstract class BaseMvpFragment<P extends AbsBusinessPresenter> extends BaseFragment implements IBusinessView {


    private P mPresenter;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mPresenter = createPresenter();
        if (mPresenter != null) {
            mPresenter.setView(this);
        }


    }

    protected abstract P createPresenter();

    public P getPresenter() {
        return this.mPresenter;
    }

}
