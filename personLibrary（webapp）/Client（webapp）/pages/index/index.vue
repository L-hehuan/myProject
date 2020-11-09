<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="book_place">
			<text>图书中心</text>
		</view>
		<view class="cu-bar search bg-white">
			<!-- 搜索框 -->
			<view class="search-form round">
				<text class="cuIcon-search"></text>
				<input v-model="search" placeholder="请输入你想搜索的图书" />
			</view>
			<view class="action">
				<button @tap="gosearch()" class="cuIcon-search" style="font-size: 100%;background-color: #e0e0e0;border: 1upx solid #e0e0e0;"></button>
			</view>
		</view>

		<swiper style="height: 500upx;margin-top: 5upx;" class="square-dot" :circular="true" :indicator-dots="true">
			<swiper-item class="flex justify-center align-center" v-for="(item,index) in banners" :key="index">
				<image @tap="gotodetail(item.wbookid)" mode="scaleToFill" class="swiper-img" :src="item.wbookimage"></image>
			</swiper-item>
		</swiper>
		<view class="bg-white tuijian">
			<view style="display: flex;align-items: center;">
				<image style="width: 50upx;height: 50upx;margin-right: 5upx;" src="../../static/img/ritui.png"></image>
				<text style="font-weight: bold;font-size: 110%;">每日推荐</text>
			</view>
			<view @tap="gowtcontent()" class="text-gray">
				查看全部<text class="cuIcon-right"></text>
			</view>
		</view>
		<view class="img-father bg-white">
			<view @tap="gocagetory(index)" v-for="(item,index) in imgLists" :key="index" class="img-item">
				<image :src="item.url"></image>
				<view style="text-align: center;">
					{{item.name}}
				</view>
			</view>

		</view>
		<view class="img-father_2 bg-white">
			<view @tap="gocagetory_2(index)" v-for="(item,index) in imgLists_2" :key="index" class="img-item">
				<image :src="item.url"></image>
				<view style="text-align: center;">
					{{item.name}}
				</view>
			</view>
		</view>
		<view class="bg-white grid-rand" style="margin-top: 10upx;">
			<view class="" style="margin-left: 10upx;">
				<image style="width: 50upx;height: 50upx;margin: 0 5upx -13upx 0upx;" src="../../static/img/rand.png"></image>
				随便看看
			</view>
		</view>
		<view class="grid">
			<view :class v-for="(p,i) in goods" :key="i">
				<image @tap="gotodetail(p.wbookid)" style="width: 236.8upx;height: 350upx;" :src="p.wbookimage"></image>
			</view>
		</view>
		<view class="flex justify-center" style="border: 1px dashed #FFFFFF;margin-top: 10upx;border-radius: 10px;background-color: #FFFFFF;">
			<image style="width: 100%;height: 80upx;" src="../../static/img/dibufoot.png"></image>
		</view>

	</view>
</template>

<script>
	import helper from '../../common/until.js';
	export default {
		// components: {
		// 	uniLoadMore //注册组件
		// },
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
				book_types: [{
					url: "../../static/img/wenxue.png",
					name: "文学"
				}, {
					url: "../../static/img/xiaoshuo.png",
					name: "小说"
				}, {
					url: "../../static/img/xinli.png",
					name: "心理"
				}, {
					url: "../../static/img/dili.png",
					name: "地理"
				}, {
					url: "../../static/img/kepu.png",
					name: "科普"
				}, {
					url: "../../static/img/lishi.png",
					name: "历史"
				}, {
					url: "../../static/img/zhexue.png",
					name: "哲学"
				}, {
					url: "../../static/img/jingji.png",
					name: "经济"
				}, {
					url: "../../static/img/renwu.png",
					name: "人物"
				}],
				selected: 0,
			}
		},
		onLoad() {
			this.getbanners();
			this.geticonLists();
			this.geticonLists_2();
			this.getbook();
			setTimeout(function() {
			}, 1000);
			//uni.startPullDownRefresh();
			uni.startPullDownRefresh({
				success: function(res) { //success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画

		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			setTimeout(function() {
				uni.stopPullDownRefresh(); //停止下拉刷新动画
			}, 1000);
			this.getbanners();
			this.getbook();
		},

		onReady() {

		},
		methods: {
			gocagetory(item) {
				var data = "";
				var url = this.imgLists[item].url_re;
				if (url != null && url != undefined) {
					uni.navigateTo({
					    url: url,
						animationType:"slide-in-bottom",
						animationDuration:500
					});
				}else{
					uni.showToast({
						title: '暂未开放',
						icon:"loading"
					});
				}
			},
			gocagetory_2(item) {
				var data = "";
				var url = this.imgLists_2[item].url_re;
				if (url != null && url != undefined) {
					uni.navigateTo({
					    url: url,
						animationType:"slide-in-bottom",
						animationDuration:500
					});
				}else{
					uni.showToast({
						title: '暂未开放',
						icon:"loading"
					});
				}
			},
			// 获取推荐内容
			gowtcontent() {
				var dataid = "";
				var data = "";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					dataid = data.wuserid;
				} catch (e) {
					//TODO handle the exception
				}
				if (data != "") {
					uni.request({
						url: helper.baseUrl + "/index/tuijian",
						data: {
							userid: dataid
						},
						method: "POST",
						success: (res) => {
							
						},
						fail: (res) => {
							uni.showToast({
								icon:"none",
								title:"网络连接出错"
							})
						}
						
					});
					uni.navigateTo({
					    url: "./wtcontent",
						animationType:"slide-in-left",
						animationDuration:500
					});

				} else {
					uni.showModal({
						title: '提示',
						content: '未登录,是否进行登录',
						success: function(res) {
							if (res.confirm == true) {
								uni.reLaunch({
									url: "../login/login"
								})
							} else if (res.cancel == true) {
								uni.showToast({
									icon: "none",
									title: "登录取消"
								})
							}
						}
					});
				}

			},
			gosearch() {
				var jsstr = "";
				uni.request({
					url: helper.baseUrl + "/index/search",
					data: {
						search: this.search
					},
					method: "POST",
					success: (res) => {
						if (res.data.status == 1) {
							uni.showToast({
								icon: "none",
								title: res.data.desc
							})
						} else {
							uni.showToast({
									icon: "none",
									title: res.data.desc
								}),
								jsstr = JSON.stringify(res.data.data);
							uni.setStorage({
								key: "searchbook",
								data: jsstr,
								success() {
									uni.navigateTo({
									    url: "./search-result",
										animationType:"slide-in-left",
										animationDuration:500
									});
								},
								fail() {
									// console.log('失败了')
								}
							})
						}
					},
					fail: (res) => {
						uni.showToast({
							icon:"none",
							title:"网络连接出错"
						})
					}
				})
			},
			gotodetail(id) {
				uni.navigateTo({
					url: `../bookdata/bookdata?id=${id}`,
					animationType:"zoom-fade-out",
					animationDuration:500
				})
			},
			qiehuan(index) {
				this.thistab = index;

			},

			//获得轮播图的数据
			getbanners() {
				var banner=[];
				var data="";
				uni.request({
					url: helper.baseUrl + "/index/banner",
					data: {

					},
					success: (res) => {
						banner = JSON.stringify(res.data);
						uni.setStorage({
							key: "bannerim",
							data: banner,
							success() {},
							fail() {}
						});
						try {
							const res = uni.getStorageSync('bannerim');
							data = JSON.parse(res);
							this.banners = data;
						} catch (e) {
							//TODO handle the exception
						};
					},
					fail: (res) => {
						try {
							const res = uni.getStorageSync('bannerim');
							data = JSON.parse(res);
							this.banners = data;
						} catch (e) {
							//TODO handle the exception
						};
					}
				})

			},
			//获取图标列表
			geticonLists() {
				var data = [{
					url: "../../static/img/book_rest.png",
					name: "全部分类",
					url_re: "../bookdata/bookcagetory"
				}, {
					url: "../../static/img/wenxue.png",
					name: "文学"
				}, {
					url: "../../static/img/xiaoshuo.png",
					name: "小说"
				}, {
					url: "../../static/img/xinli.png",
					name: "心理"
				}, {
					url: "../../static/img/dili.png",
					name: "地理"
				}];
				this.imgLists = data;
			},
			geticonLists_2() {
				var data = [{
					url: "../../static/img/kepu.png",
					name: "科普"
				}, {
					url: "../../static/img/lishi.png",
					name: "历史"
				}, {
					url: "../../static/img/zhexue.png",
					name: "哲学"
				}, {
					url: "../../static/img/jingji.png",
					name: "经济"
				}, {
					url: "../../static/img/renwu.png",
					name: "人物"
				}];
				this.imgLists_2 = data;
			},
			getbook() {
				var good=""
				var goodim=[]
				var data=""
				uni.request({
					url: helper.baseUrl + "/index/randbook",
					data: {

					},
					success: (res) => {
						good = JSON.stringify(res.data);
						uni.setStorage({
							key: "goodim",
							data: good,
							success() {},
							fail() {}
						});
						try {
							const res = uni.getStorageSync('goodim');
							data = JSON.parse(res);
							this.goods = data;
						} catch (e) {
							//TODO handle the exception
						};
					},
					fail: (res) => {
						try {
							const res = uni.getStorageSync('goodim');
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
		}
	}
</script>

<style>
	.grid-rand {
		height: 70upx;
		display: grid;
		grid-template-columns: 1fr;
		margin-bottom: 10upx;
		margin-top: 10upx;
		font-size: 120%;
		align-items: center;
		font-weight: bold;
	}

	.grid {
		margin-top: 10upx;
		height: 750upx;
		display: grid;
		grid-gap: 20upx;
		grid-template-columns: 1fr 1fr 1fr;
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
		height: 130upx;
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
		font-size: 120%;
		margin: 20upx 20upx 50upx 0;
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
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}
</style>
