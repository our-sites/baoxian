package com.bao361.insurance.ui.recycler.holders;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v7.widget.RecyclerView;
import android.view.View;

import com.bao361.insurance.ui.recycler.AbsAdapterGroup;
import com.bao361.insurance.ui.recycler.dataset.IDataSetGroup;


public abstract class ChildViewHolder<G, C> extends AbsViewHolder {

    private IDataSetGroup.Index mIndex;

    public ChildViewHolder(Context context, @Nullable RecyclerView parent) {
        super(context, parent);
    }

    protected ChildViewHolder(Context context, @NonNull RecyclerView parent, int layout) {
        super(context, parent, layout);
    }

    protected ChildViewHolder(Context context, @Nullable RecyclerView parent, View itemView) {
        super(context, parent, itemView);
    }

    @Override
    protected void onItemPositionChanged(int position) {
        super.onItemPositionChanged(position);
        mIndex = getDataSet().turnChildIndex(position);
    }

    @Override
    public final void onBindViewHolder(int position) {
        onBindViewHolder(position, mIndex.groupIndex, getGroup(), mIndex.childIndex, getChild());
    }

    protected abstract void onBindViewHolder(int position, int gIndex, G group, int cIndex, C child);

    private G getGroup() {
        return getDataSet().getGroup(mIndex.groupIndex);
    }

    private C getChild() {
        return getDataSet().getChild(mIndex.groupIndex, mIndex.childIndex);
    }

    @Override
    public final void onItemClick(int position) {
        onItemClick(position, mIndex.groupIndex, getGroup(), mIndex.childIndex, getChild());
    }

    protected void onItemClick(int position, int gindex, G group, int cIndex, C child) {
    }

    @Override
    public final boolean onItemLongClick(int position) {
        return onItemLongClick(position, mIndex.groupIndex, getGroup(), mIndex.childIndex, getChild());
    }

    protected boolean onItemLongClick(int position, int gIndex, G group, int cIndex, C child) {
        return false;
    }

    private IDataSetGroup<G, C> getDataSet() {
        return (IDataSetGroup<G, C>) getAdapter(AbsAdapterGroup.class).getDataSet();
    }

    public void sendMessageChild(String key) {
        sendMessageChild(key, null);
    }

    public void sendMessageChild(String key, Bundle args) {
        AbsAdapterGroup<G, C> adapter = getAdapter(AbsAdapterGroup.class);
        adapter.sendMessageChild(key, getItemPosition(), mIndex.groupIndex, getGroup(), mIndex.childIndex, getChild(), args);
    }

}
