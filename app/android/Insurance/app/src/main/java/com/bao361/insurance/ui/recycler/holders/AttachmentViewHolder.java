package com.bao361.insurance.ui.recycler.holders;

import android.content.Context;
import android.support.annotation.Nullable;
import android.support.v7.widget.RecyclerView;
import android.view.View;

public class AttachmentViewHolder extends AbsViewHolder {

    public AttachmentViewHolder(Context context, @Nullable RecyclerView parent) {
        super(context, parent);
    }

    public AttachmentViewHolder(Context context, @Nullable RecyclerView parent, int layout) {
        super(context, parent, layout);
    }

    public AttachmentViewHolder(Context context, View view) {
        super(context, null, view);
    }

    @Override
    protected void onViewCreated(View itemView) {

    }

    @Override
    public void onBindViewHolder(int position) {

    }

    @Override
    public void onItemClick(int position) {

    }

    @Override
    public boolean onItemLongClick(int position) {
        return false;
    }

}
