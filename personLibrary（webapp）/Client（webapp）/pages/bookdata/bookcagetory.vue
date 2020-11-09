<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">  
		    <view class="top_view"></view>  
		</view>  
		<!-- #endif -->
		<view class="book_read_top">
			<view @tap="goindex()" class="cuIcon-back cu-btn bg-white" style="padding-left: 10upx;">
			</view>
			<view class="" style="margin-right: 310upx;">
				<text>图书分类</text>
			</view>
			
		</view>
		<!-- <cu-custom bgColor="bg-gradual-pink" :isBack="true">
			<block slot="backText">返回</block>
			<block slot="content">导航栏</block>
		</cu-custom> -->
		<view v-for="(item,index) in goods" :key="index" v-if="index==TabCur" class="bg-grey padding margin text-center">
			当前位置:<text>{{item.wyname}}</text>
		</view>
		<scroll-view scroll-x class="bg-white nav" scroll-with-animation :scroll-left="scrollLeft">
			<view class="cu-item" :style="{fontSize:TabCur==index?'120%':'100%'}" :id="'book-'+index" :class="index==TabCur?'text-green cur':''" v-for="(item,index) in goods" :key="index" @tap="tabSelect" :data-id="index">
				{{item.wyname}}
			</view>
		</scroll-view>
		
		<!-- <scroll-view scroll-x class="bg-white nav" scroll-with-animation :scroll-left="scrollLeft">
			<view :style="{fontSize:selected==index?'120%':'100%'}" :id="'book-'+index" class="cu-item" :class="index==selected?'text-green cur':''" v-for="(item,index) in goods" :key="index" @tap="select(index)"
			 :data-id="index">
				{{item.wyname}}
			</view>
		</scroll-view>
		<view class="flex" style="">
			<!-- <scroll-view class="" scroll-y style="height: calc(100vh - 210upx);width: 200upx;">
				<view @tap="select(i)" :style="{fontSize:selected==i?'120%':'100%'}" :class="selected==i?'bg-white text-bold':''"
				 v-for="(p,i) in goods" :key="i" class="type-item">
					<view v-if="selected==i" class="shuxian"></view>{{p.wyname}}
				</view>
			</scroll-view> -->
			<scroll-view scroll-with-animation :scroll-into-view="'book-'+TabCur" class="bg-white" scroll-y style="height: calc(100vh - 210upx);">
				<view :id="'book-'+i" v-if="i==TabCur" v-for="(p,i) in goods" :key="i" class="" style="border-bottom: 0.5upx #e7e7e7 solid;padding-bottom: 40upx;">
					<view class="text-bold text-black g-title">
					</view>
					<view class="flex flex-wrap" >
						<view @tap="gotodetail(tp.wbookid)" v-for="(tp,ti) in p.data" :key="ti" class="flex justify-center align-center"
						 style="width: 250upx;margin-top: 10upx;">
							<view class="">
								<image style="width: 200upx;height: 300upx;" :src="tp.wbookimage"></image>
								<view class="flex justify-center align-center flex-direction">
									<view class="" style="text-align: center;width: 200upx;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">{{tp.wbookname}}</view>
								</view>
		
							</view>
		
						</view>
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		data() {
			return {
				text: 'uni-app',
				shu: null,
				search: "",
				thistab: 0,
				jsons: [],
				jsons_1: [],
				banners: [],
				imgLists: [],
				goods: [],
				goodsLists: [],
				imgLists_2: [],
				all_book: [],
				types: [],
				selected: 0,
				TabCur: 0,
				scrollLeft: 0
			}
		},
		methods: {
			tabSelect(e) {
				this.TabCur = e.currentTarget.dataset.id;
				this.scrollLeft = (e.currentTarget.dataset.id - 1) * 60;
			},
			goindex() {
				var url = "../index/index";
				if (url != null && url != undefined) {
					uni.reLaunch({
						url: url
					});
				}
			
			},
			gotodetail(id) {
				uni.navigateTo({
					url: `../bookdata/bookdata?id=${id}`,
					animationType:"zoom-fade-out",
					animationDuration:500
				})
			},
			getbook() {
				var god=""
				var godim=[]
				var data=""
				uni.request({
					url: helper.baseUrl + "/user/types",
					data: {
					},
					success: (res) => {
						god = JSON.stringify(res.data);
						uni.setStorage({
							key: "godim",
							data: god,
							success() {},
							fail() {}
						});
						try {
							const res = uni.getStorageSync('godim');
							data = JSON.parse(res);
							this.goods = data;
						} catch (e) {
							//TODO handle the exception
						};
					},
					fail: (res) => {
						try {
							const res = uni.getStorageSync('godim');
							data = JSON.parse(res);
							this.goods = data;
						} catch (e) {
							//TODO handle the exception
						};
					}
				})
			},
			select(i) {
				this.selected = i;
			}
		},
		onLoad() {
			this.getbook();
			setTimeout(function() {
				// console.log('start pulldown');
			}, 1000);
			//uni.startPullDownRefresh();
			uni.startPullDownRefresh({
				success:function(res) {
					// console.log(res); //success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画
		
		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			        // console.log('refresh');
			        setTimeout(function () {
			            uni.stopPullDownRefresh();  //停止下拉刷新动画
			        }, 1000);
					this.getbook();
		},
		
		onReady() {
		
		},
	}
</script>

<style>
	.book_read_top {
		height: 70upx;
		display: flex;
		justify-content: space-between;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-bottom: 5upx;
	}
	.newslist {
		padding: 10px;
		line-height: 60px;
		font-size: 28px;
	}
	
	.loading {
		text-align: center;
		line-height: 80px;
	}
	
	.swiper-img {
		width: 350upx;
		height: 500upx;
	}
	
	.tuijian {
		display: flex;
		justify-content: space-between;
		height: 160upx;
		align-items: center;
		padding-left: 20upx;
		padding-right: 20upx;
	}
	
	.img-item image {
		width: 100upx;
		height: 100upx;
	}
	
	.img-father {
		border-top: 0.5upx solid #e7e7e7;
		display: flex;
		justify-content: space-around;
		padding-top: 30upx;
		padding-bottom: 10upx;
	}
	
	.img-father_2 {
	
		display: flex;
		justify-content: space-around;
		padding-top: 10upx;
		padding-bottom: 30upx;
	}
	
	.tuijian-father {
		margin-top: 20upx;
	}
	
	.tejiabar {
		padding-left: 20upx;
		padding-right: 20upx;
	}
	
	.image1 {
		width: 130upx;
		height: 130upx;
	}
	
	.type-item {
		height: 100upx;
		text-align: center;
		line-height: 100upx;
		position: relative;
	}
	
	.shuxian {
		position: absolute;
		width: 12upx;
		height: 40upx;
		background-color: red;
		top: 30upx;
		left: 10upx;
	}
	
	.g-title {
		font-size: 140%;
		margin: 25upx 25upx 20upx 20upx;
		text-align: center;
		font-weight: bold;
		color: white;
		border-radius: 20px;
		background-color: #333333;
	}
	
	.zhanwei {
		height: var(--status-bar-height);
		width: 100%;
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
