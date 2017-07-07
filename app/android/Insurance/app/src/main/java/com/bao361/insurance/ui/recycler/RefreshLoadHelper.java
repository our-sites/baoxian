package com.bao361.insurance.ui.recycler;

import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.ListView;

import com.bao361.insurance.R;

public class RefreshLoadHelper extends LoadHelper {

    private SwipeRefreshLayout mRefreshLayout;

    public static interface OnRefreshLoadListener extends SwipeRefreshLayout.OnRefreshListener, OnLoadListener {
    }

    @Deprecated
    public RefreshLoadHelper(SwipeRefreshLayout refresh, ListView listView) {
        this(refresh, listView, null);
    }

    @Deprecated
    public RefreshLoadHelper(SwipeRefreshLayout refresh, ListView listView, View footerView) {
        super(listView, footerView);
        this.mRefreshLayout = refresh;
        this.mRefreshLayout.setColorSchemeResources(R.color.colorAccent);
    }

    public RefreshLoadHelper(SwipeRefreshLayout refresh, RecyclerView recyclerView) {
        this(refresh, recyclerView, null);
        this.mRefreshLayout = refresh;
        this.mRefreshLayout.setColorSchemeResources(R.color.colorAccent);
    }

    public RefreshLoadHelper(SwipeRefreshLayout refresh, RecyclerView recyclerView, View footerView) {
        super(recyclerView, footerView);
        this.mRefreshLayout = refresh;
        this.mRefreshLayout.setColorSchemeResources(R.color.colorAccent);
    }

    /*
        Settings: Enable
     */

    public void setEnable(boolean enable) {
        setEnableRefresh(enable);
        setEnableLoad(enable);
    }

    public boolean isEnable() {
        return isEnableRefresh() && isEnableLoad();
    }

    public void setEnableRefresh(boolean refresh) {
        mRefreshLayout.setEnabled(refresh);
    }

    public boolean isEnableRefresh() {
        return mRefreshLayout.isEnabled();
    }

    @Override
    public boolean isEnableLoad() {
        return !isRefreshing() && super.isEnableLoad();
    }

    /*cd
        /Settings: Enable
     */

    /*
       /Settings: state
    */
    public void setRefreshing(boolean refreshing) {
        mRefreshLayout.setRefreshing(refreshing);
    }

    public boolean isRefreshing() {
        return mRefreshLayout.isRefreshing();
    }

    public void setOnRefreshLoadListener(OnRefreshLoadListener listener) {
        super.setOnLoadListener(listener);
        mRefreshLayout.setOnRefreshListener(listener);
    }

    @Override
    public void setOnLoadListener(OnLoadListener listener) {
        throw new RuntimeException("For RefreshLoadHelper, use setOnRefreshLoadListener(OnRefreshLoadListener)");
    }
}
