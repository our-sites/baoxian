package com.bao361.insurance.modules.main.fragment;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.bao361.insurance.R;
import com.bao361.insurance.base.BaseMvpFragment;
import com.bao361.insurance.modules.main.models.QuestionModel;
import com.bao361.insurance.modules.main.presenter.QuestionPresenter;
import com.bao361.insurance.modules.main.viewholder.QuestionHolder;
import com.bao361.insurance.modules.main.viewimpl.QuestionView;
import com.bao361.insurance.ui.recycler.AbsAdapter;
import com.bao361.insurance.ui.recycler.RefreshLoadHelper;
import com.bao361.insurance.ui.widget.DividerDecoration;

import java.util.ArrayList;

/**
 * Created by wangyongchao on 2017/8/30.
 * 问吧
 */

public class QuestionFragment extends BaseMvpFragment<QuestionPresenter> implements QuestionView, RefreshLoadHelper.OnRefreshLoadListener {

    private AbsAdapter<QuestionModel> mAdapter;
    private RefreshLoadHelper refreshLoadHelper;

    private View loadingView;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {


        return inflater.inflate(R.layout.fragment_question, null);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {

        SwipeRefreshLayout swipeRefreshLayout = (SwipeRefreshLayout) view.findViewById(R.id.swipeRefresh);
        RecyclerView mRecyclerView = (RecyclerView) view.findViewById(R.id.recycler_view);
        mRecyclerView.setHasFixedSize(true);
        mRecyclerView.addItemDecoration(new DividerDecoration(getContext()));
        mRecyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));

        loadingView = view.findViewById(R.id.loading_view);


        refreshLoadHelper = new RefreshLoadHelper(swipeRefreshLayout, mRecyclerView);
        refreshLoadHelper.setEnableRefresh(false);
        refreshLoadHelper.setOnRefreshLoadListener(this);
        mAdapter = new AbsAdapter<QuestionModel>(getActivity(), QuestionHolder.class);
        mRecyclerView.setAdapter(mAdapter);

        getPresenter().loadData();

    }

    @Override
    public void setLoadingIndicator(boolean active) {
        if (active) {
            loadingView.setVisibility(View.VISIBLE);
        } else {
            loadingView.setVisibility(View.GONE);
        }

    }

    @Override
    public boolean refresh() {
        return false;
    }

    @Override
    protected QuestionPresenter createPresenter() {
        return new QuestionPresenter();
    }

    @Override
    public void onRefresh() {

    }

    @Override
    public void onLoad() {

    }

    @Override
    public void setData(ArrayList<QuestionModel> models) {
        mAdapter.getDataSet().addAll(models);
        mAdapter.notifyDataSetChanged();
    }
}
