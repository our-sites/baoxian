package com.bao361.insurance.ui.recycler.holders.creator;


import com.bao361.insurance.ui.recycler.holders.ChildViewHolder;
import com.bao361.insurance.ui.recycler.holders.GroupViewHolder;

public interface ViewHolderCreatorGroup<G, C> {

    public int getGroupHolder(int position, int groupIndex, G group);

    public Class<? extends GroupViewHolder<G,C>> getGroupHolder(int viewType);

    public int getChildHolder(int position, int groupIndex, int childIndex, C child);

    public Class<? extends ChildViewHolder<G,C>> getChildHolder(int viewType);
}
