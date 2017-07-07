package com.bao361.insurance.ui.recycler.holders;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v7.widget.RecyclerView;
import android.view.View;

import com.bao361.insurance.ui.recycler.AbsAdapter;

import java.util.List;

public abstract class ItemViewHolder<Data> extends AbsViewHolder {

    public ItemViewHolder(Context context, @Nullable RecyclerView parent) {
        super(context, parent);
    }

    protected ItemViewHolder(Context context, @NonNull RecyclerView parent, int layout) {
        super(context, parent, layout);
    }

    protected ItemViewHolder(Context context, @Nullable RecyclerView parent, View itemView) {
        super(context, parent, itemView);
    }

    @Override
    public final void onBindViewHolder(int position) {
        onBindViewHolder(position, getData());
    }

    protected abstract void onBindViewHolder(int position, Data data);

    private Data getData() {
        return (Data) getAdapter(AbsAdapter.class).getData(getItemPosition());
    }

    protected final List<Data> getDataSet() {
        return (List<Data>) getAdapter(AbsAdapter.class).getDataSet();
    }

    @Override
    public final void onItemClick(int position) {
        onItemClick(position, getData());
    }

    protected void onItemClick(int position, Data data) {
    }

    @Override
    public final boolean onItemLongClick(int position) {
        return onItemLongClick(position, getData());
    }

    protected boolean onItemLongClick(int position, Data data) {
        return false;
    }

    public final void sendMessage(String key) {
        sendMessage(key, null);
    }

    public final void sendMessage(String key, Bundle args) {
        AbsAdapter<Data> adapter = getAdapter(AbsAdapter.class);
        adapter.sendMessage(key, getItemPosition(), getData(), args);
    }

}
