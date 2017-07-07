package com.bao361.insurance.ui.recycler.holders;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v7.widget.RecyclerView;
import android.view.View;

import com.bao361.insurance.ui.recycler.AbsAdapterGroup;
import com.bao361.insurance.ui.recycler.dataset.IDataSetGroup;

import java.util.List;

public abstract class GroupViewHolder<G, C> extends AbsViewHolder {

    private int mGroupIndex;

    public GroupViewHolder(Context context, @Nullable RecyclerView parent) {
        super(context, parent);
    }

    protected GroupViewHolder(Context context, @NonNull RecyclerView parent, int layout) {
        super(context, parent, layout);
    }

    protected GroupViewHolder(Context context, @Nullable RecyclerView parent, View itemView) {
        super(context, parent, itemView);
    }

    @Override
    protected void onItemPositionChanged(int position) {
        super.onItemPositionChanged(position);
        mGroupIndex = getDataSet().turnGroupIndex(position);
    }

    @Override
    public final void onBindViewHolder(int position) {
        onBindViewHolder(position, mGroupIndex, getGroup(), getChilds());
    }

    protected abstract void onBindViewHolder(int position, int gIndex, G group, List<C> childs);

    @Override
    public final void onItemClick(int position) {
        onItemClick(position, mGroupIndex, getGroup(), getChilds());
    }

    protected void onItemClick(int position, int gIndex, G group, List<C> childs) {
    }

    @Override
    public final boolean onItemLongClick(int position) {
        return onItemLongClick(position, mGroupIndex, getGroup(), getChilds());
    }

    protected boolean onItemLongClick(int position, int gIndex, G group, List<C> childs) {
        return false;
    }

    protected final int getGroupIndex() {
        return mGroupIndex;
    }

    private IDataSetGroup<G, C> getDataSet() {
        return (IDataSetGroup<G, C>) getAdapter(AbsAdapterGroup.class).getDataSet();
    }

    private G getGroup() {
        return getDataSet().getGroup(mGroupIndex);
    }

    private List<C> getChilds() {
        return getDataSet().getChilds(mGroupIndex);
    }

    public void sendMessageGroup(String key) {
        sendMessageGroup(key, null);
    }

    public void sendMessageGroup(String key, Bundle args) {
        AbsAdapterGroup<G, C> adapter = getAdapter(AbsAdapterGroup.class);
        adapter.sendMessageGroup(key, getItemPosition(), mGroupIndex, getGroup(), getChilds(), args);
    }

}
