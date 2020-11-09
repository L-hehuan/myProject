<template>
	<view class="bg-white">
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">  
		    <view class="top_view"></view>  
		</view>  
		<!-- #endif -->
		<!-- 吸顶 -->
		<view class="userim-top">
			<view @tap="goindex()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				图书中心
			</view>
			<view class="book_place" style="padding-left: 10upx;">
				<text >搜索结果</text>
			</view>
			
		</view>
		<view class="bg-white padding">
			<view class="grid margin-bottom text-center" :class="'col-' + 1">
				<view class="bg-cyan padding">搜索结果</view>
				<view class="bg-blue padding">为你找到以下书籍</view>

			</view>
		</view>
		<view class="search-top padding ">
			<view @tap="gotodetail(item.wbookid)" style="height: 800upx;border: 3px solid #e0e0e0;margin-bottom: 20upx;"
			 v-for="(item,index) in bookresult" :key="index" class="search-result padding">
			     <view class="flex justify-center align-center">
			     	<image style="width: 400upx;" :src="item.wbookimage"></image>
			     </view>
				<view class="flex justify-around align-center ">
					<view class="">
						<text style="font-weight: 900;color: red;">书名:</text>{{item.wbookname}}
					</view>
					<view class="">
						<text style="font-weight: 900;color: red;">作者:</text>{{item.wbookauthor}}
					</view>
					<view class="">
						<text style="font-weight: 900;color: red;">馆藏编号:</text>0{{item.wbookid}}
					</view>
				</view>
			</view>
		</view>

	</view>
</template>

<script>
	import helper from "../../common/until.js"
	export default {
		data() {
			return {
				text:'uni-app',
				bookresult: [],
				lensearchbook: 0

			}
		},
		onLoad() {
			this.getsearchbook();
		},
		methods: {
			getsearchbook() {
				var data = [];
				try {
					const res = uni.getStorageSync('searchbook');
					data = JSON.parse(res);
					this.bookresult = data;
				} catch (e) {
					//TODO handle the exception
				}
			},
			goindex() {
				uni.reLaunch({
					url: "./index"
				})
			},
			gotodetail(id) {
				uni.navigateTo({
					url: `../bookdata/bookdata-search?id=${id}`,
					animationType:"zoom-fade-out",
					animationDuration:500
				})
			}

		}
	}
</script>

<style>
	.userim-top{
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 120upx;
	}
	.xiding {
		width: 100%;
		height: var(--status-bar-height);
	}

	.anniu {
		width: 80upx;
		height: 80upx;
		padding: 8upx 8upx;
		border-radius: 80upx;
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: rgba(41, 36, 33, 0.2);
	}

	.comeback {
		height: 100upx;
		background-color: red;
	}

	.search-result image {
		height: 650upx;
	}
	.status_bar {
	    height: var(--status-bar-height);  
	    width: 100%;  
	    background-color: #F8F8F8;  
	}  
	.top_view {  
	    height: var(--status-bar-height);  
	    width: 100%;  
	    position: fixed;  
	    background-color: #F8F8F8;  
	    top: 0;  
	    z-index: 999;  
	}
</style>
