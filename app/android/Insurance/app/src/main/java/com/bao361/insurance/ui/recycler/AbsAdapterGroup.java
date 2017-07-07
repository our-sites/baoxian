package com.bao361.insurance.ui.recycler;

import android.content.Context;
import android.os.Bundle;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.view.ViewGroup;

import com.bao361.insurance.ui.recycler.attachment.AttachmentGroup;
import com.bao361.insurance.ui.recycler.dataset.DataSetGroup;
import com.bao361.insurance.ui.recycler.dataset.IDataSetGroup;
import com.bao361.insurance.ui.recycler.holders.AbsViewHolder;
import com.bao361.insurance.ui.recycler.holders.ChildViewHolder;
import com.bao361.insurance.ui.recycler.holders.GroupViewHolder;
import com.bao361.insurance.ui.recycler.holders.creator.ViewHolderCreatorGroup;
import com.bao361.insurance.ui.recycler.superslim.GridSLM;
import com.bao361.insurance.ui.recycler.superslim.LayoutManager;

import java.util.List;

public class AbsAdapterGroup<G, C> extends RecyclerView.Adapter<AbsViewHolder> {

    private static final int GROUP_START = Integer.MIN_VALUE + 50000;
    private final static int GROUP_DISPLAY = LayoutManager.LayoutParams.HEADER_INLINE | LayoutManager.LayoutParams.HEADER_STICKY;

    private final Context mContext;
    private final IDataSetGroup<G, C> mDataSet;
    private final ViewHolderCreatorGroup<G, C> mVHCreator;
    private final AttachmentGroup mAttachment;

    private Bundle mArguments;
    private MessageHandlerGroup<G, C> mMessageHandlerGroup;

    public static interface MessageHandlerGroup<G, C> {
        public void handlerMessageGroup(String key, int position, int gIndex, G group, List<C> childs, Bundle args);

        public void handlerMessageChild(String key, int position, int gIndex, G group, int cIndex, C child, Bundle args);
    }

    // todo item click
    private class ItemClickListener implements View.OnClickListener, View.OnLongClickListener {
        private final AbsViewHolder mHolder;

        public ItemClickListener(AbsViewHolder holder) {
            mHolder = holder;
            mHolder.itemView.setOnClickListener(this);
            mHolder.itemView.setOnLongClickListener(this);
        }

        @Override
        public void onClick(View v) {
            int position = mHolder.getAdapterPosition();
            if (position < RecyclerView.NO_POSITION) {
                return;
            }
            mHolder.onItemClick(mHolder.getItemPosition());
        }

        @Override
        public boolean onLongClick(View v) {
            int position = mHolder.getAdapterPosition();
            if (position < RecyclerView.NO_POSITION) {
                return false;
            }
            mHolder.onItemLongClick(mHolder.getItemPosition());
            return false;
        }
    }

    public AbsAdapterGroup(Context ctx, ViewHolderCreatorGroup<G, C> vhCreator) {
        this.mContext = ctx;
        this.mVHCreator = vhCreator;
        this.mAttachment = new AttachmentGroup(ctx);
        this.mDataSet = new DataSetGroup<>();
    }

    public AbsAdapterGroup(Context ctx, final Class<? extends GroupViewHolder<G, C>> vhGHolder, final Class<? extends ChildViewHolder<G, C>> vhCHolder) {
        this(ctx, new ViewHolderCreatorGroup<G, C>() {
            @Override
            public int getGroupHolder(int position, int groupIndex, G g) {
                return 0;
            }

            @Override
            public Class<? extends GroupViewHolder<G, C>> getGroupHolder(int viewType) {
                return vhGHolder;
            }

            @Override
            public int getChildHolder(int position, int groupIndex, int childIndex, C c) {
                return 0;
            }

            @Override
            public Class<? extends ChildViewHolder<G, C>> getChildHolder(int viewType) {
                return vhCHolder;
            }

        });
    }

    public Context getContext() {
        return mContext;
    }

    public IDataSetGroup<G, C> getDataSet() {
        return this.mDataSet;
    }

    public AttachmentGroup getAttachment() {
        return mAttachment;
    }

    // --------------- ItemType
    @Override
    public final int getItemViewType(int position) {
        if (mAttachment.isAttachment(position, mDataSet.size())) {
            return getItemViewTypeAttachment(position);
        } else {
            return getItemViewTypeDataSet(position);
        }
    }

    protected int getItemViewTypeAttachment(int position) {
        return mAttachment.getItemViewType(position, mDataSet.size());
    }

    private int getItemViewTypeDataSet(int position) {
        position = position - mAttachment.getHeaderCount();
        if (mDataSet.isGroup(position)) {
            int gIndex = mDataSet.turnGroupIndex(position);
            return getItemViewTypeGroup(position, gIndex);
        } else {
            IDataSetGroup.Index cIndex = mDataSet.turnChildIndex(position);
            return getItemViewTypeChild(position, cIndex.groupIndex, cIndex.childIndex);
        }
    }

    protected int getItemViewTypeGroup(int position, int gIndex) {
        G group = mDataSet.getGroup(gIndex);
        return mVHCreator.getGroupHolder(position, gIndex, group) + GROUP_START;
    }

    protected int getItemViewTypeChild(int position, int gIndex, int cIndex) {
        C child = mDataSet.getChild(gIndex, cIndex);
        return mVHCreator.getChildHolder(position, gIndex, cIndex, child);
    }

    // --------------- /ItemType

    @Override
    public AbsViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        AbsViewHolder viewHolder;
        if (mAttachment.isAttachmentType(viewType)) {
            viewHolder = mAttachment.getItemViewHolder(viewType);
        } else {
            // isGroup
            if (viewType >= GROUP_START && viewType < GROUP_START + mDataSet.sizeOfGroup()) {
                Class<? extends AbsViewHolder> vhClass = mVHCreator.getGroupHolder(viewType - GROUP_START);
                viewHolder = createViewHolder(vhClass, parent);
            } else {
                Class<? extends AbsViewHolder> vhClass = mVHCreator.getChildHolder(viewType);
                viewHolder = createViewHolder(vhClass, parent);
            }
        }
//        viewHolder.setArguments(mArguments);
//        viewHolder.bindAdapter(this);
        viewHolder.onViewCreated(viewHolder.itemView, mArguments, this);
        new ItemClickListener(viewHolder);
        return viewHolder;
    }

    private AbsViewHolder createViewHolder(Class<? extends AbsViewHolder> vhClass, ViewGroup parent) {
        try {
            return vhClass.getConstructor(Context.class, RecyclerView.class).newInstance(getContext(), parent);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    // --------------- BindViewHolder
    @Override
    public void onBindViewHolder(AbsViewHolder holder, final int position) {
        int firstPosition;
        int fixPosition;
        if (mAttachment.isAttachment(position, mDataSet.size())) {
            fixPosition = position;
//            onBindViewHolderAttachment((AttachmentViewHolder) holder, position);
            if (mAttachment.isHeader(position)) {
                firstPosition = 0;
            } else /*if (mAttachment.isFooter(position, mDataSet.size()))*/ {
                firstPosition = mAttachment.getHeaderCount() + mDataSet.size();
            }
        } else {
            fixPosition = position - mAttachment.getHeaderCount();
//            onBindViewHolderDataSet(holder, fixPosition);
            firstPosition = mDataSet.getGroupPosition(fixPosition) + mAttachment.getHeaderCount();
        }


        final View itemView = holder.itemView;
        final GridSLM.LayoutParams stickyParams = GridSLM.LayoutParams.from(itemView.getLayoutParams());
        stickyParams.headerDisplay = GROUP_DISPLAY;
        stickyParams.isHeader = position == firstPosition;
        stickyParams.setFirstPosition(firstPosition);
        itemView.setLayoutParams(stickyParams);

        holder.setItemPosition(fixPosition);
        holder.onBindViewHolder(fixPosition);
    }

//    private void onBindViewHolderDataSet(AbsViewHolder holder, int position) {
//        final boolean isGroup = mDataSet.isGroup(position);
//        if (isGroup) {
//            onBindViewHolderGroup(holder, position);
//        } else {
//            onBindViewHolderChild(holder, position);
//        }
//    }
//
//    private void onBindViewHolderGroup(AbsViewHolder holder, int position) {
//        GroupViewHolder<G, C> vh = (GroupViewHolder<G, C>) holder;
//        int gIndex = mDataSet.turnGroupIndex(position);
//        G group = mDataSet.getGroup(gIndex);
//        holder.setItemPosition(position);
////        holder.setItemPosition(position, gIndex, -1);
////        vh.onBindViewHolderGroup(group);
//        holder.onBindViewHolder(position);
//    }
//
//    private void onBindViewHolderChild(AbsViewHolder holder, int position) {
//        ChildViewHolder<G, C> vh = (ChildViewHolder<G, C>) holder;
//        IDataSetGroup.Index cIndex = mDataSet.turnChildIndex(position);
//        C child = mDataSet.getChild(cIndex.groupIndex, cIndex.childIndex);
//
//        holder.setItemPosition(position);
////        holder.setItemPosition(position, cIndex.groupIndex, cIndex.childIndex);
////        vh.onBindViewHolder(child);
//        holder.onBindViewHolder(position);
//    }
    // --------------- /BindViewHolder

    @Override
    public int getItemCount() {
        return mDataSet.size() + mAttachment.getCount();
    }

    public void setArguments(Bundle bundle) {
        this.mArguments = bundle;
    }

    public void sendMessageGroup(String key, int position, int gIndex, G group, List<C> childs, Bundle args) {
        if (mMessageHandlerGroup != null) {
            mMessageHandlerGroup.handlerMessageGroup(key, position, gIndex, group, childs, args);
        }
    }

    public void sendMessageChild(String key, int position, int gIndex, G group, int cIndex, C child, Bundle args) {
        if (mMessageHandlerGroup != null) {
            mMessageHandlerGroup.handlerMessageChild(key, position, gIndex, group, cIndex, child, args);
        }
    }

    public void setMessageHandlerGroup(MessageHandlerGroup<G, C> handler) {
        this.mMessageHandlerGroup = handler;
    }
}
