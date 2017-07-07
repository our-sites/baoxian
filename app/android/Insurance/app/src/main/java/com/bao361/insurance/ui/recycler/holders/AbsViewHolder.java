package com.bao361.insurance.ui.recycler.holders;

import android.content.Context;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;

import com.bao361.insurance.ui.recycler.AbsAdapter;

/**
 * ViewHolder抽象基类<br/>
 * 创建时会调用 {@link AbsViewHolder#AbsViewHolder(Context, RecyclerView)} 构造器,<br/>
 * 子类应覆写次构造器后调用其它构造器 {@link #AbsViewHolder(Context, RecyclerView, int)} 或 {@link #AbsViewHolder(Context, RecyclerView, View)}<br/>
 * RecyclerView.ViewHolder 必须在创建时给予一个View<p/>
 */
public abstract class AbsViewHolder extends RecyclerView.ViewHolder {

    private static final String LOG_TAG = "AbsViewHolder";

    private Context mContext;
    private RecyclerView.Adapter<?> mAdapter;

    private int mItemPosition = -1;
    private Bundle mArguments;

    private boolean onViewCreated;

    /**
     * 必须重写此构造器,调用其他构造器来传递 View
     * View 必须传进来,否则会抛出异常
     * <p>
     * 如果你有更好的想法请联系我(longjun.cui)
     *
     * @param context
     */
    public AbsViewHolder(Context context, @Nullable RecyclerView parent) {
        super(null);
    }

    protected AbsViewHolder(Context context, @NonNull RecyclerView parent, int layout) {
        this(context, parent, LayoutInflater.from(context).inflate(layout, parent, false));
    }

    protected AbsViewHolder(Context context, @Nullable RecyclerView parent, View itemView) {
        super(itemView);
        this.mContext = context;
    }

    public Context getContext() {
        return mContext;
    }

    public final void onViewCreated(View itemView, Bundle args, RecyclerView.Adapter bindAdapter) {
        if (!onViewCreated) {
            onViewCreated = true;
            setArguments(args);
            bindAdapter(bindAdapter);
            onViewCreated(itemView);
        }
    }

    /**
     * 跟随 ViewHolder 创建时调用
     *
     * @param itemView
     */
    protected abstract void onViewCreated(View itemView);

    /**
     * ViewHolder 被重复利用时调用
     *
     * @param position 已去除 Header 和 Footer 的position
     */
    public final void setItemPosition(int position) {
        mItemPosition = position;
        onItemPositionChanged(mItemPosition);
    }

    /**
     * 已去除 Header 和 Footer 的position
     *
     * @return
     */
    public final int getItemPosition() {
        return mItemPosition;
    }

    /**
     * 在 {@link AbsAdapter#setArguments(Bundle)} 中设置的 Bundle
     *
     * @param bundle
     */
    private final void setArguments(Bundle bundle) {
        mArguments = bundle;
    }

    protected final Bundle getArguments() {
        return mArguments;
    }

    /**
     * <p>
     * !!! 需要注意类型转换问题
     *
     * @param key
     * @param <T>
     * @return
     */
    protected <T> T getArgument(String key) {
        if (mArguments == null) {
            Log.e("LOG_TAG", "getArgument(key) --> arguments == null");
            return null;
        }
        return (T) mArguments.get(key);
    }

    /**
     * @see #setItemPosition(int)
     */
    protected void onItemPositionChanged(int position) {
    }

    /**
     * {@link AbsAdapter} 创建ViewHolder后把自身放进来,用来访问数据等<br/>
     * 不要自己调用
     *
     * @param adapter
     */
    private final void bindAdapter(RecyclerView.Adapter adapter) {
        if (this.mAdapter != null) {
            throw new RuntimeException("已经绑定过一次Adapter了");
        }
        this.mAdapter = adapter;
    }

    /**
     * 为了不让随意访问Adaper 故把访问与写成 default,保持隔离性<br/>
     *
     * @param c
     * @param <T>
     * @return
     */
    /*default*/ <T extends RecyclerView.Adapter> T getAdapter(Class<T> c) {
        return (T) mAdapter;
    }

    /**
     * 同 {@link android.support.v7.widget.RecyclerView.Adapter#onBindViewHolder(RecyclerView.ViewHolder, int)}
     *
     * @param position 已过滤 Header 和 Footer positon
     */
    public abstract void onBindViewHolder(int position);

    public abstract void onItemClick(int position);

    public abstract boolean onItemLongClick(int position);

    /**
     * 同  {@link RecyclerView.Adapter#notifyDataSetChanged()}
     */
    public final void notifyDataSetChanged() {
        getAdapter(RecyclerView.Adapter.class).notifyDataSetChanged();
    }

}
