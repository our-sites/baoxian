package com.bao361.insurance.ui.recycler;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.view.ViewGroup;

import com.bao361.insurance.ui.recycler.attachment.Attachment;
import com.bao361.insurance.ui.recycler.holders.AbsViewHolder;
import com.bao361.insurance.ui.recycler.holders.AttachmentViewHolder;
import com.bao361.insurance.ui.recycler.holders.ItemViewHolder;
import com.bao361.insurance.ui.recycler.holders.creator.ViewHolderCreator;

import java.util.ArrayList;
import java.util.List;

public class AbsAdapter<Data> extends RecyclerView.Adapter<AbsViewHolder> {

    private final Context mContext;
    private final List<Data> mDataSet;
    private final ViewHolderCreator<Data> mVHCreator;
    private final Attachment mAttachment;

    private OnItemClickListener<Data> mOnItemClickListener;
    private OnItemLongClickListener<Data> mOnItemLongClickListener;

    private Bundle mArguments;
    private MessageHandler<Data> mMessageHandler;

    public static interface OnItemClickListener<Data> {
        /**
         * @param position
         * @param data
         * @return true viewhoder 的 click 事件不会被触发
         */
        public boolean onItemClick(int position, Data data);
    }

    public static interface OnItemLongClickListener<Data> {
        public boolean onItemLongClick(int position, Data data);
    }

    /**
     * 消息处理器
     *
     * @param <Data>
     */
    public static interface MessageHandler<Data> {
        /**
         * @param key
         * @param position 点击的位置
         * @param item
         * @param args
         */
        public void handlerMessage(String key, int position, Data item, Bundle args);
    }

    private class ItemClickListener implements View.OnClickListener, View.OnLongClickListener {
        private final AbsViewHolder mHolder;

        private ItemClickListener(AbsViewHolder holder) {
            mHolder = holder;
            mHolder.itemView.setOnClickListener(this);
            mHolder.itemView.setOnLongClickListener(this);
        }

        @Override
        public void onClick(View v) {
            onHandlerClick(true);
        }

        @Override
        public boolean onLongClick(View v) {
            return onHandlerClick(false);
        }

        private boolean onHandlerClick(boolean isFast) {
            int position = mHolder.getAdapterPosition();
            if (position < RecyclerView.NO_POSITION) {
                return false;
            }
            if (mHolder instanceof ItemViewHolder) {
                int pos = mHolder.getItemPosition();
                boolean handler = false;
                if ((isFast && mOnItemClickListener != null) || (!isFast && mOnItemLongClickListener != null)) {
                    Data data = getData(pos);
                    if (data != null) {
                        handler = isFast ? mOnItemClickListener.onItemClick(pos, data) : mOnItemLongClickListener.onItemLongClick(pos, data);
                    }
                }
                if (!handler) {
                    if (isFast) {
                        handler = true;
                        mHolder.onItemClick(pos);
                    } else {
                        handler = mHolder.onItemLongClick(pos);
                    }
                }
                return handler;
            } else if (mHolder instanceof AttachmentViewHolder) {
                if (isFast) {
                    mHolder.onItemClick(position);
                    return true;
                } else {
                    return mHolder.onItemLongClick(position);
                }
            }
            return false;
        }
    }

    public AbsAdapter(Context ctx, @NonNull ViewHolderCreator<Data> vhCreator) {
        this(ctx, vhCreator, new ArrayList<Data>());
    }

    public AbsAdapter(Context ctx, @NonNull ViewHolderCreator<Data> vhCreator, List<Data> dataset) {
        this.mContext = ctx;
        this.mDataSet = dataset;
        this.mVHCreator = vhCreator;
        this.mAttachment = new Attachment(ctx);
    }

    public AbsAdapter(Context ctx, @NonNull final Class<? extends ItemViewHolder<Data>> vhClass, List<Data> dataset) {
        this(ctx, new ViewHolderCreator<Data>() {
            @Override
            public int getItemViewType(int position, Data data) {
                return 0;
            }

            @Override
            public Class<? extends ItemViewHolder<Data>> getItemViewHolder(int viewType) {
                return vhClass;
            }
        }, dataset);
    }

    public AbsAdapter(Context ctx, @NonNull final Class<? extends ItemViewHolder<Data>> vhClass) {
        this(ctx, vhClass, new ArrayList<Data>());
    }

    public final Context getContext() {
        return mContext;
    }

    public Attachment getAttachment() {
        return mAttachment;
    }

    public void setArguments(Bundle bundle) {
        this.mArguments = bundle;
    }

    // --------------- ItemType
    @Override
    public final int getItemViewType(int position) {
        System.out.println("getItemViewType position="+position);
        if (mAttachment.isAttachment(position, mDataSet.size())) {
            return getItemViewTypeAttachment(position);
        } else {
            return getItemViewTypeDataSet(position);
        }
    }

    protected int getItemViewTypeAttachment(int position) {
        return mAttachment.getItemViewType(position, mDataSet.size());
    }

    protected int getItemViewTypeDataSet(int position) {
        position = position - mAttachment.getHeaderCount();
        Data data = mDataSet.get(position);
        return mVHCreator.getItemViewType(position, data);
    }
    // --------------- /ItemType

    public Data getData(int position) {
        if (mDataSet == null || mDataSet.isEmpty() || mDataSet.size() <= position) {
            return null;
        }
        return mDataSet.get(position);
    }

    public List<Data> getDataSet() {
        return mDataSet;
    }

    @Override
    public final AbsViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        System.out.println("onCreateViewHolder viewType="+viewType);
        AbsViewHolder viewHolder;
        if (mAttachment.isAttachmentType(viewType)) {
            AttachmentViewHolder vh = mAttachment.getItemViewHolder(viewType);
            viewHolder = vh;
        } else {
            Class<? extends ItemViewHolder<Data>> vhClass = mVHCreator.getItemViewHolder(viewType);
            try {
                ItemViewHolder<Data> vh = vhClass.getConstructor(Context.class, RecyclerView.class).newInstance(getContext(), parent);
                viewHolder = vh;
            } catch (Exception e) {
                Throwable cause = e.getCause();
                if (cause != null) {
                    throw new RuntimeException(cause);
                } else {
                    throw new RuntimeException(e);
                }
            }
        }
//        viewHolder.setArguments(mArguments);
//        viewHolder.bindAdapter(this);
        viewHolder.onViewCreated(viewHolder.itemView, mArguments, this);
        new ItemClickListener(viewHolder); // TODO FIX
        return viewHolder;
    }

    // --------------- BindViewHolder
    @Override
    public final void onBindViewHolder(AbsViewHolder holder, int position) {
        System.out.println();
        if (mAttachment.isAttachment(position, mDataSet.size())) {
//            onBindViewHolderAttachment((AttachmentViewHolder) holder, position);
        } else if (!mDataSet.isEmpty()) {
//            onBindViewHolderDataSet(holder, position - mAttachment.getHeaderCount());
            position -= mAttachment.getHeaderCount();
        }
        holder.setItemPosition(position);
//        holder.setArguments(mArguments);
        holder.onBindViewHolder(position);
    }

    /**
     * @deprecated 不要使用这个方法, 要拿到count {@link #getDataCount()}
     */
    @Override
    @Deprecated
    public final int getItemCount() {
        System.out.println("getItemCount");
        return getDataCount() + mAttachment.getCount();
    }

    @Override
    public long getItemId(int position) {
        System.out.println("getItemId position="+position);
        return super.getItemId(position);
    }

    public int getDataCount() {
        if (mDataSet == null || mDataSet.isEmpty()) {
            return 0;
        }
        return mDataSet.size();
    }

    // --------------- /

    public void setOnItemClickListener(OnItemClickListener<Data> listener) {
        this.mOnItemClickListener = listener;
    }

    public void setOnItemLongClickListener(OnItemLongClickListener<Data> listener) {
        this.mOnItemLongClickListener = listener;
    }

    /**
     * 用于ViewHolder发送给 MessageHandler
     *
     * @param key
     * @param position
     * @param data
     * @param args
     */
    public final void sendMessage(String key, int position, Data data, Bundle args) {
        if (mMessageHandler != null) {
            mMessageHandler.handlerMessage(key, position, data, args);
        }
    }

    public final void setMessageHandler(MessageHandler handler) {
        this.mMessageHandler = handler;
    }
}
