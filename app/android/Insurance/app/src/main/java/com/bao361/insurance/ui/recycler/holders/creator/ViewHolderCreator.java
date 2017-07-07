package com.bao361.insurance.ui.recycler.holders.creator;

import com.bao361.insurance.ui.recycler.holders.ItemViewHolder;

/**
 * ViewHolder创建器
 */
public interface ViewHolderCreator<T> {

    public int getItemViewType(int position, T data);

    public Class<? extends ItemViewHolder<T>> getItemViewHolder(int viewType);
}
