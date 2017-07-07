package com.bao361.insurance.modules.main;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.View;

import com.bao361.insurance.R;
import com.bao361.insurance.base.BaseActivity;
import com.bao361.insurance.ui.recycler.AbsAdapter;
import com.bao361.insurance.ui.recycler.LoadHelper;
import com.bao361.insurance.ui.recycler.RefreshLoadHelper;

import java.util.ArrayList;

public class RecyclerViewActivity extends BaseActivity implements View.OnClickListener, RefreshLoadHelper.OnRefreshLoadListener {
    private AbsAdapter<String> mAdapter;
    private RecyclerView mRecyclerView;
    private ArrayList<String> data;
    private SwipeRefreshLayout swipeRefreshLayout;

    private Handler handler = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            mAdapter.notifyDataSetChanged();
            refreshLoadHelper.setRefreshing(false);
            refreshLoadHelper.setLoading(LoadHelper.LOADING_IDLE);

        }
    };
    private RefreshLoadHelper refreshLoadHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recycler);

        initView();

        data = getData();
    }

    private void initView() {

        this.findViewById(R.id.btn).setOnClickListener(this);
        swipeRefreshLayout = (SwipeRefreshLayout) findViewById(R.id.swipeRefresh);
        mRecyclerView = (RecyclerView) findViewById(R.id.recycler_view);
        mRecyclerView.setHasFixedSize(true);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));


        refreshLoadHelper = new RefreshLoadHelper(swipeRefreshLayout, mRecyclerView);
        refreshLoadHelper.setLoading(LoadHelper.LOADING_IDLE);

        refreshLoadHelper.setOnRefreshLoadListener(this);
        mAdapter = new AbsAdapter<String>(this, TestHolder.class);


        mRecyclerView.setAdapter(mAdapter);

    }

    private void loadData(final boolean isRefresh) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    if (isRefresh) {
                        mAdapter.getDataSet().add(0, "第一条");
                    } else {
                        mAdapter.getDataSet().add("最后一条");
                    }

                    Thread.sleep(1000);
                    handler.sendEmptyMessage(0);

                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();


    }

    @Override
    public void onClick(View v) {
        mAdapter.getDataSet().addAll(data);
        mAdapter.notifyDataSetChanged();
    }

    private ArrayList<String> getData() {
        ArrayList<String> ss = new ArrayList<>();
        for (int i = 0; i < 20; i++) {
            ss.add("aa" + i);
        }
        return ss;
    }


    @Override
    public void onRefresh() {
        loadData(true);

    }

    @Override
    public void onLoad() {
        loadData(false);
    }
}
