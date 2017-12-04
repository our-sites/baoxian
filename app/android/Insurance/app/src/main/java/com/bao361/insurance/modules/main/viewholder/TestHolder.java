package com.bao361.insurance.modules.main.viewholder;

import android.content.Context;
import android.support.annotation.Nullable;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.TextView;

import com.bao361.insurance.ui.recycler.holders.ItemViewHolder;

public class TestHolder extends ItemViewHolder<String> {

    private TextView textView;

    public TestHolder(Context context, @Nullable RecyclerView parent) {
        super(context, parent, android.R.layout.simple_list_item_1);
    }

    @Override
    protected void onBindViewHolder(int i, String s) {
        textView.setText(s);

    }

    @Override
    protected void onItemClick(int i, String s) {


    }

    @Override
    protected void onViewCreated(View view) {
        textView = (TextView) view.findViewById(android.R.id.text1);

    }

}
