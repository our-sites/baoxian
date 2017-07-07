package com.bao361.insurance.base;

import android.os.Bundle;
import android.support.v4.app.Fragment;

public abstract class BaseFragment<P extends AbsBusinessPresenter> extends Fragment implements IBusinessView {


    private P mPresenter;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mPresenter = createPresenter();
        mPresenter.setView(this);

    }

    protected abstract P createPresenter();

    public P getPresenter() {
        return this.mPresenter;
    }

}
