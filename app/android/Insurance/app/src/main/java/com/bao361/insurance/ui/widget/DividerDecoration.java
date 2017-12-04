package com.bao361.insurance.ui.widget;

import android.content.Context;
import android.graphics.Rect;
import android.support.v7.widget.RecyclerView;
import android.view.View;

import com.bao361.insurance.utils.InsuranceUtils;

public class DividerDecoration extends RecyclerView.ItemDecoration {
    private int mHeight;

    public DividerDecoration(Context context) {
        mHeight = InsuranceUtils.dip2px(context, 10);
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
        super.getItemOffsets(outRect, view, parent, state);
        outRect.bottom = mHeight;
    }
}