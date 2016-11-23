package com.common.insurance.modules.main;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.common.insurance.R;
import com.common.insurance.base.BaseActivity;

import butterknife.BindView;

public class MainActivity extends BaseActivity<MainPresenter> implements View.OnClickListener, MainView {

    @BindView(R.id.fengzhuangpost)
    Button mButton;


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
                getPresenter().sendEncapsulationPost();
                break;
        }

    }

    @Override
    protected MainPresenter createPresenter() {
        return new MainPresenter();
    }


    @Override
    public void setLoadingIndicator(boolean active) {

    }

    @Override
    public boolean refresh() {
        return false;
    }


    @Override
    public void setText() {

    }
}
