package com.bao361.insurance.ui.recycler.dataset;

import java.util.ArrayList;
import java.util.List;



public class DataSetGroup<G, C> implements IDataSetGroup<G, C> {

    private List<ItemData> mDataSet = new ArrayList<>();
    private List<G> mGroupDataSet = new ArrayList<>();
    private List<List<C>> mChildDataSet = new ArrayList<>();

    class ItemData {
        final int groupIndex;
        final int groupPosition;
        final boolean isGroup;
        final int childIndex;

        ItemData(int groupIndex, int groupPosition) {
            this.groupIndex = groupIndex;
            this.groupPosition = groupPosition;
            this.isGroup = true;
            this.childIndex = -1;
        }

        ItemData(int groupIndex, int groupPosition, int childIndex) {
            this.groupIndex = groupIndex;
            this.groupPosition = groupPosition;
            this.isGroup = false;
            this.childIndex = childIndex;
        }
    }

    public DataSetGroup() {
    }

    @Override
    public int size() {
        return mDataSet.size();
    }

    @Override
    public int sizeOfGroup() {
        return mGroupDataSet.size();
    }

    @Override
    public int sizeOfChild(int groupIndex) {
        if (groupIndex >= mChildDataSet.size() || groupIndex < 0) {
            return -1;
        }
        List<C> childList = mChildDataSet.get(groupIndex);
        if (childList == null) {
            return 0;
        }
        return childList.size();
    }

    @Override
    public int turnGroupIndex(int position) {
        if (!isLegalPosition(position)) {
            return -1;
        }
        return getItem(position).groupIndex;
    }

    @Override
    public int getGroupPosition(int position) {
        if (!isLegalPosition(position)) {
            return -1;
        }
        return getItem(position).groupPosition;
    }

    @Override
    public Index turnChildIndex(int position) {
        if (!isLegalPosition(position)) {
            return null;
        }
        ItemData data = getItem(position);
        return new Index(data.groupIndex, data.childIndex);
    }

    @Override
    public boolean isGroup(int position) {
        if (!isLegalPosition(position)) {
            return false;
        }
        return getItem(position).isGroup;
    }

    @Override
    public void setDataSet(List<G> groups, List<List<C>> childs) {
        clear();
        if (groups != null) {
            mGroupDataSet.addAll(groups);
        }
        if (childs != null) {
            mChildDataSet.addAll(childs);
        }
        resetDataSet();
    }

    @Override
    public void addGroup(G group, List<C> childs) {
        mGroupDataSet.add(group);
        mChildDataSet.add(childs);
        resetDataSet();
    }

    @Override
    public void addChilds(G group, List<C> childs) {
        int gIndex = mGroupDataSet.indexOf(group);
        if (gIndex == -1) {
            return;
        }
        addChilds(gIndex, childs);
    }

    @Override
    public void addChilds(int groupIndex, List<C> childs) {
        if (groupIndex < 0 || groupIndex >= mGroupDataSet.size() || childs == null || childs.isEmpty()) {
            return;
        }
        List<C> childList = mChildDataSet.get(groupIndex);
        if (childList == null) {
            childList = new ArrayList<>();
            mChildDataSet.set(groupIndex, childList);
        }
        childList.addAll(childs);
        resetDataSet();
    }

    @Override
    public void setChilds(int groupIndex, List<C> childs) {
        if (groupIndex >= mGroupDataSet.size()) {
            return;
        }
        List<C> childList = mChildDataSet.get(groupIndex);
        if (childList == null) {
            childList = new ArrayList<>();
        }
        childList.clear();
        if (childs != null) {
            childList.addAll(childs);
        }
        mChildDataSet.set(groupIndex, childList);
        resetDataSet();
    }

    @Override
    public void setChilds(G group, List<C> childs) {
        int gIndex = mGroupDataSet.indexOf(group);
        if (gIndex == -1) {
            return;
        }
        setChilds(gIndex, childs);
    }

    @Override
    public void addChild(G group, C child) {
        int gIndex = mGroupDataSet.indexOf(group);
        if (gIndex == -1) {
            return;
        }
        addChild(gIndex, child);
    }

    @Override
    public void addChild(int groupIndex, C child) {
        if (groupIndex >= mGroupDataSet.size()) {
            return;
        }
        List<C> childList = mChildDataSet.get(groupIndex);
        if (childList == null) {
            childList = new ArrayList<>();
            mChildDataSet.set(groupIndex, childList);
        }
        childList.add(child);
        resetDataSet();
    }

    @Override
    public int indexOf(G group) {
        return mGroupDataSet.indexOf(group);
    }

    @Override
    public G getGroup(int groupIndex) {
        if (groupIndex >= mGroupDataSet.size()) {
            return null;
        }
        return mGroupDataSet.get(groupIndex);
    }

    @Override
    public List<G> getGroups() {
        return new ArrayList<>(mGroupDataSet);
    }

    @Override
    public C getChild(int groupIndex, int childIndex) {
        if (groupIndex >= mChildDataSet.size()) {
            return null;
        }
        List<C> childList = mChildDataSet.get(groupIndex);
        if (childList == null || childIndex >= childList.size()) {
            return null;
        }
        return mChildDataSet.get(groupIndex).get(childIndex);
    }

    @Override
    public List<C> getChilds(int groupIndex) {
        if (groupIndex >= mChildDataSet.size()) {
            return null;
        }

        List<C> list = mChildDataSet.get(groupIndex);

        if (list == null) {
            return null;
        }

        return new ArrayList<>(list);
    }

    @Override
    public void removeGroup(int groupIndex) {
        if (groupIndex >= mGroupDataSet.size()) {
            return;
        }
        mGroupDataSet.remove(groupIndex);
        mChildDataSet.remove(groupIndex);
        resetDataSet();
    }

    @Override
    public void removeChild(int groupIndex, int childIndex) {
        if (groupIndex >= mGroupDataSet.size()) {
            return;
        }
        List<C> childList = mChildDataSet.get(groupIndex);
        if (childList == null || childIndex >= childList.size()) {
            return;
        }
        childList.remove(childIndex);
        resetDataSet();
    }

    @Override
    public void clear() {
        mDataSet.clear();
        mGroupDataSet.clear();
        mChildDataSet.clear();
    }

    @Override
    public void clearChilds(int groupIndex) {
        if (mChildDataSet.size() <= groupIndex) {
            return;
        }
        List<C> childs = mChildDataSet.get(groupIndex);
        if (childs != null) {
            childs.clear();
        }
        resetDataSet();
    }

    @Override
    public boolean isEmpty() {
        return mDataSet.isEmpty();
    }

    @Override
    public boolean isEmptyChilds(int groupIndex) {
        if (groupIndex >= mChildDataSet.size()) {
            return true;
        }
        List<C> childList = mChildDataSet.get(groupIndex);
        return childList == null || childList.isEmpty();
    }

    private boolean isLegalPosition(int position) {
        return position < mDataSet.size();
    }

    private ItemData getItem(int position) {
        return mDataSet.get(position);
    }

    private void resetDataSet() {
        mDataSet.clear();

        int groupPosition = 0;
        for (int groupIndex = 0; groupIndex < mGroupDataSet.size(); groupIndex++) {
            List<C> childList = (mChildDataSet == null || mChildDataSet.isEmpty() || mChildDataSet.size() <= groupIndex) ? null : mChildDataSet.get(groupIndex);
            if (childList == null && mChildDataSet != null) {
                mChildDataSet.add(childList = new ArrayList<C>());
            }
            if (childList != null) {
                mDataSet.add(new ItemData(groupIndex, groupPosition));
                for (int childIndex = 0; childIndex < childList.size(); childIndex++) {
                    mDataSet.add(new ItemData(groupIndex, groupPosition, childIndex));
                }
                groupPosition += childList.size() + 1;
            }
        }
    }

}
