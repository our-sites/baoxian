package com.bao361.insurance.ui.recycler;

import android.content.Context;
import android.support.annotation.IntDef;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.AttributeSet;
import android.view.View;
import android.widget.AbsListView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;


import com.bao361.insurance.R;
import com.bao361.insurance.ui.recycler.holders.AttachmentViewHolder;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.util.ArrayList;
import java.util.List;


public class LoadHelper {

    private AbsListView.OnScrollListener mListViewScrollListener;
    private boolean mLoadEnable = true;
    @Deprecated
    private ListView mListView;
    @Deprecated
    private List<View> mBelowListFooterView;

    private RecyclerView mRecyclerView;
    private List<AttachmentViewHolder> mBelowFooterView;
    private View mFooterView;

    private final boolean isRecycler;

    // 默认终止,避免第一次刷新时同事触发loading,RefreshLoadHelper不存在此问题
    private int mLoading = LOADING_END;

    @IntDef({LOADING_IDLE, LOADING, LOADING_END, LOADING_FAIL})
    @Retention(RetentionPolicy.SOURCE)
    public @interface LoadingState {
    }

    private OnLoadListener mOnLoadListener;
    private OnFooterClickListener mOnFooterClickListener;

    public static interface OnLoadListener {
        public void onLoad();
    }

    public static interface OnFooterClickListener {
        public boolean onClick(int loadingState);
    }

    public static final int LOADING_END = 0;
    public static final int LOADING_IDLE = 1;
    public static final int LOADING = 2;
    public static final int
            LOADING_FAIL = -1;

    public static interface FooterView {
        public void onLoadingIdle();

        public void onLoading();

        public void onLoadingEnd();

        public void onLoadingFail();
    }

    /**
     * ------------------------
     * ListView
     * ------------------------
     */
    /**
     * @deprecated 用 {@link android.support.v7.widget.RecyclerView.Recycler} 吧..
     */
    @Deprecated
    public LoadHelper(ListView listView) {
        this(listView, null);
    }

    /**
     * @deprecated 用 {@link android.support.v7.widget.RecyclerView.Recycler} 吧..
     */
    @Deprecated
    public LoadHelper(ListView listView, View footerView) {
        isRecycler = false;
        mListView = listView;
        setupListView(listView, footerView);
    }

    @Deprecated
    private void setupListView(final ListView listView, View footerView) {
        mListView = listView;
        mListView.post(new Runnable() {
            @Override
            public void run() {
                listView.setOnScrollListener(new AbsListView.OnScrollListener() {
                    @Override
                    public void onScrollStateChanged(AbsListView view, int scrollState) {
                        if (mListViewScrollListener != null) {
                            mListViewScrollListener.onScrollStateChanged(view, scrollState);
                        }
                    }

                    @Override
                    public void onScroll(AbsListView view, int firstVisibleItem, int visibleItemCount, int totalItemCount) {
                        if (mListViewScrollListener != null) {
                            mListViewScrollListener.onScroll(view, firstVisibleItem, visibleItemCount, totalItemCount);
                        } // is mListView.isAttachedToWindow();

                        if (/*isRefreshing() || */!isEnableLoad() || isLoading() || isLoadingEnd() || isLoadingFail() || visibleItemCount == 0) {
                            // if( 刷新中 || 禁用加载 || 加载中 || 加载完成|| 加载直白 || visible 0)
                            return;
                        }
                        int lastVisibleItem = firstVisibleItem + visibleItemCount;
                        if (lastVisibleItem + 2 >= totalItemCount) {
                            // TODO (totalItemCount - 2) 之内滑动应该也进行
                            // 未加载 && 不是最后一个 && 倒数第二个
                            notifyLoad();
                        }
                    }
                });
            }
        });
        final View foot;
        if (footerView == null) {
            foot = new DefaultListViewFooter(listView.getContext());
        } else {
            foot = footerView;
        }
        mListView.post(new Runnable() {
            @Override
            public void run() {
                setFooterView(foot);
                if (mBelowListFooterView != null && !mBelowListFooterView.isEmpty()) {
                    for (View view : mBelowListFooterView) {
                        mListView.addFooterView(view);
                    }
                }
            }
        });
    }

    @Deprecated
    public void addHolderBelowFooter(View view) {
        if (mBelowListFooterView == null) {
            mBelowListFooterView = new ArrayList<>();
        }
        mBelowListFooterView.add(view);
    }

    @Deprecated
    public void removeViewBelowFooter(View view) {
        if (mBelowListFooterView == null || mBelowListFooterView.isEmpty()) {
            return;
        }
        mBelowListFooterView.remove(view);
        mListView.removeFooterView(view);
    }

    /**
     * @deprecated 用 {@link android.support.v7.widget.RecyclerView.Recycler} 吧..
     */
    @Deprecated
    public void setOnListViewScrollListener(AbsListView.OnScrollListener listener) {
        mListViewScrollListener = listener;
    }

    public void setListFooterView(View view) {
        view.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                onClickFooterView();
            }

        });
        mListView.addFooterView(view);
    }

    /**
     * ------------------------
     * /ListView
     * ------------------------
     */

    /**
     * ------------------------
     * RecyclerView
     * ------------------------
     */

    public LoadHelper(RecyclerView recyclerView) {
        this(recyclerView, new DefaultListViewFooter(recyclerView.getContext()));
    }

    public LoadHelper(RecyclerView recyclerView, View footerView) {
        isRecycler = true;
        mRecyclerView = recyclerView;
        setupRecyclerView(recyclerView, footerView);
    }

    private void setupRecyclerView(RecyclerView recyclerView, View footerView) {
        recyclerView.addOnScrollListener(new RecyclerView.OnScrollListener() {
            @Override
            public void onScrollStateChanged(RecyclerView recyclerView, int newState) {
                super.onScrollStateChanged(recyclerView, newState);


            }

            @Override
            public void onScrolled(RecyclerView recyclerView, int dx, int dy) {
                super.onScrolled(recyclerView, dx, dy);
                RecyclerView.LayoutManager lm = recyclerView.getLayoutManager();
                int lastVisibleItem;
                int visibleItemCount;
                if (lm instanceof LinearLayoutManager) {
                    lastVisibleItem = ((LinearLayoutManager) lm).findLastVisibleItemPosition();
                    int firstVisibleItem = ((LinearLayoutManager) lm).findFirstVisibleItemPosition();
                    visibleItemCount = ((LinearLayoutManager) lm).findLastVisibleItemPosition() - firstVisibleItem;
//                } else if (lm instanceof LayoutManager) {
//                    firstVisibleItem = ((LayoutManager) lm).findFirstVisibleItemPosition();
//                    visibleItemCount = ((LayoutManager) lm).findLastVisibleItemPosition() - firstVisibleItem;
                } else {
                    throw new RuntimeException("没有被兼容的 LayoutManager! className: " + lm.getClass().getName());
                }

                if (/*isRefreshing() || */!isEnableLoad() || isLoading() || isLoadingEnd() || isLoadingFail() || visibleItemCount == 0) {
                    // if( 刷新中 || 禁用加载 || 加载中 || 加载完成|| 加载直白 || visible 0)
                    return;
                }

                RecyclerView.Adapter adapter = recyclerView.getAdapter();
                if (lastVisibleItem + 2 >= adapter.getItemCount()) {
                    notifyLoad();
                }

            }
        });

        final View foot;
        if (footerView == null) {
            foot = new DefaultListViewFooter(recyclerView.getContext());
        } else {
            foot = footerView;
        }

        mRecyclerView.post(new Runnable() {
            @Override
            public void run() {
                AbsAdapter adapter = (AbsAdapter) mRecyclerView.getAdapter();
                int sPosition = adapter.getItemCount();
                setFooterView(foot);
                int belowCount = 0;
                if (mBelowFooterView != null && !mBelowFooterView.isEmpty()) {
                    for (AttachmentViewHolder holder : mBelowFooterView) {
                        adapter.getAttachment().addFooter(holder);
                    }
                    belowCount = mBelowFooterView.size();
                }
                adapter.notifyItemRangeInserted(sPosition, 1 + belowCount);
//                adapter.notifyDataSetChanged();
            }
        });
    }

    public void addHolderBelowFooter(AttachmentViewHolder holder) {
        if (mBelowFooterView == null) {
            mBelowFooterView = new ArrayList<>();
        }
        mBelowFooterView.add(holder);
    }

    public void setRecyclerFooterView(View footerView) {
        AbsAdapter adapter = (AbsAdapter) mRecyclerView.getAdapter();
        adapter.getAttachment().addFooter(new AttachmentViewHolder(mRecyclerView.getContext(), footerView) {
            @Override
            public void onItemClick(int position) {
                onClickFooterView();
            }
        });
    }

    /**
     * ------------------------
     * /RecyclerView
     * ------------------------
     */
    private void setFooterView(View view) {
        if (!(view instanceof FooterView)) {
            throw new IllegalArgumentException("FooterView应实现 FooterView 接口");
        }
        if (mFooterView != null) {
            mListView.removeFooterView(mFooterView);
        }
        mFooterView = view;

        setLoading(mLoading); //refresh ui
        if (isRecycler) {
            setRecyclerFooterView(view);
        } else {
            setListFooterView(view);
        }
    }

    private void onClickFooterView() {
        boolean handler = false;
        if (mOnFooterClickListener != null) {
            handler = mOnFooterClickListener.onClick(mLoading);
        }
        if (!handler) {
            if (mLoading == LOADING_FAIL) {
                notifyLoad();
            }
        }
    }

    /*
        Settings: Enable
     */

    public void setEnableLoad(boolean load) {
        mLoadEnable = load;
    }

    public boolean isEnableLoad() {
        return mLoadEnable;
    }

    /*
        /Settings: Enable
     */


    /*
        Settings: state
     */
    public void setLoading(@LoadingState int state) {
        mLoading = state;

        if (mFooterView == null) {
            return;
        }
        FooterView fv = (FooterView) mFooterView;
        switch (mLoading) {
            case LOADING:
                fv.onLoading();
                break;
            case LOADING_END:
                fv.onLoadingEnd();
                break;
            case LOADING_FAIL:
                fv.onLoadingFail();
                break;
            case LOADING_IDLE:
                fv.onLoadingEnd();
                break;
        }
    }

    public boolean isLoading() {
        return mLoading == LOADING;
    }

    public boolean isLoadingFail() {
        return mLoading == LOADING_FAIL;
    }

    public boolean isLoadingEnd() {
        return mLoading == LOADING_END;
    }

    private void notifyLoad() {
        setLoading(LOADING);
        if (mOnLoadListener != null) {
            mOnLoadListener.onLoad();
        }
    }

    public static class DefaultListViewFooter extends LinearLayout implements FooterView {

        protected Context mContext;
        protected View mProgressBar;
        protected TextView mHintView;

        public DefaultListViewFooter(Context context) {
            super(context);
            initView(context);
        }

        public DefaultListViewFooter(Context context, AttributeSet attrs) {
            super(context, attrs);
            initView(context);
        }

        private void initView(Context context) {
            mContext = context;
            View.inflate(context, R.layout.loading_footer, this);
            mProgressBar = findViewById(R.id.ios_listview_footer_progressbar);
            mHintView = (TextView) findViewById(R.id.ios_listview_footer_hint_textview);
        }

        @Override
        public void onLoadingIdle() {
            onLoadingEnd();
        }

        @Override
        public void onLoading() {
            mHintView.setVisibility(View.INVISIBLE);
            mProgressBar.setVisibility(View.VISIBLE);
        }

        @Override
        public void onLoadingEnd() {
            mProgressBar.setVisibility(View.INVISIBLE);
            mHintView.setVisibility(View.INVISIBLE);
        }

        @Override
        public void onLoadingFail() {
            mProgressBar.setVisibility(View.INVISIBLE);
            mHintView.setVisibility(View.VISIBLE);
            mHintView.setText(R.string.app_name);
        }
    }

    public void setOnLoadListener(OnLoadListener listener) {
        this.mOnLoadListener = listener;
    }

    public void setOnFooterClickListener(OnFooterClickListener listener) {
        this.mOnFooterClickListener = listener;
    }
}
