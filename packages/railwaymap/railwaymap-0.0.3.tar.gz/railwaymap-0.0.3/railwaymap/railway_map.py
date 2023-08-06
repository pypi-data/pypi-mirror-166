from pyecharts import options as opts
from pyecharts.charts import Map, Geo
from pyecharts.globals import ChartType
from pyecharts.commons.utils import JsCode
from railwaymap.json_data import china_railway_bureau_map, haerbinju, shenyangju, huhehaoteju, beijingju, wulumuqiju, \
qingzanggongsi, chengduju, kunmingju, lanzhouju, xianju, taiyuanju, zhengzhouju, jinanju, shanghaiju, nanchangju, \
guangzhouju, nanningju, wuhanju


def get_center_coordinate():
    """
    根据各路局中心点坐标，组成json数据，用于热力图坐标绘制
    :return: center_json_data
    """
    # 也可以根据需要修改字典中的路局名称以及坐标值
    center_json_data = {
        '哈尔滨局': haerbinju['features'][0]['properties']['cp'],
        '沈阳局': shenyangju['features'][0]['properties']['cp'],
        '呼和浩特局': huhehaoteju['features'][0]['properties']['cp'],
        '北京局': beijingju['features'][0]['properties']['cp'],
        '乌鲁木齐局': wulumuqiju['features'][0]['properties']['cp'],
        '青藏公司': qingzanggongsi['features'][0]['properties']['cp'],
        '成都局': chengduju['features'][0]['properties']['cp'],
        '昆明局': kunmingju['features'][0]['properties']['cp'],
        '兰州局': lanzhouju['features'][0]['properties']['cp'],
        '西安局': xianju['features'][0]['properties']['cp'],
        '太原局': taiyuanju['features'][0]['properties']['cp'],
        '郑州局': zhengzhouju['features'][0]['properties']['cp'],
        '济南局': jinanju['features'][0]['properties']['cp'],
        '上海局': shanghaiju['features'][0]['properties']['cp'],
        '南昌局': nanchangju['features'][0]['properties']['cp'],
        '广州局': guangzhouju['features'][0]['properties']['cp'],
        '南宁局': nanningju['features'][0]['properties']['cp'],
        '武汉局': wuhanju['features'][0]['properties']['cp']
    }
    return center_json_data


def blank_map(bureau_data, without_name=True):
    """
    空白显示的地图
    :param bureau_data: 路局名称和数据的list
    :param without_name: 是否显示路局名称， True=不显示，False=显示
    :return: 生成html文件，无返回值
    """
    json_data = china_railway_bureau_map
    if without_name is True:
        # 不显示路局名称和红点
        display_bureaus_name = False
    else:
        # 显示路局名称和红点
        display_bureaus_name = True
    # 定义生成文件名称
    file_name = 'China_railway_bureau_map(blank).html'
    # 定义地图参数
    map = (
        # 定义尺寸等初始设置
        Map(init_opts=opts.InitOpts(width='1000px', height='750px', bg_color='white', page_title='各路局地图'))
        # 注册地图
        .add_js_funcs("echarts.registerMap('china_railway', {});".format(json_data))
        .add(
            # 系列名称
            series_name='',
            # 数据项(坐标点名称，坐标点值)
            data_pair=bureau_data,
            # 地图类型，新注册的题图
            maptype='china_railway',
            # 是否开启鼠标缩放和平移漫游
            is_roam=True,
            # 当前视角的缩放比例。
            zoom=1,
            # 是否显示标记图形，False=取消红点显示
            is_map_symbol_show=display_bureaus_name,
            )
        # False=取消路局名称显示
        .set_series_opts(label_opts=opts.LabelOpts(is_show=display_bureaus_name))
        .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(
                # 是否显示该工具 True=显示
                is_show=True,
                # 工具栏的布局朝向:横向
                orient='horizontal',
                # 工具栏离底侧像素5
                pos_bottom='5',
                # 工具栏只显示保存图片的功能
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True, name=file_name[:-5]),
                    restore=opts.ToolBoxFeatureRestoreOpts(is_show=False),
                    data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                    magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=False),
                    brush=opts.ToolBoxFeatureBrushOpts(type_=False)
                )
            )
        )
    )
    map.render('{0}'.format(file_name))
    print('文件{0}已生成至当前路径下!'.format(file_name))


def normal_map(bureau_data):
    """
    用不同颜色代表数据的地图
    :param bureau_data: 路局名称和数据的list
    :return: 生成html文件，无返回值
    """
    # 判断json数据是否为空，也就是检查json文件是否存在
    json_data = china_railway_bureau_map
    # 计算传入数据的最大值和最小值，用于颜色显示标签
    data_list = [item[1] for item in bureau_data]
    min_data = min(data_list)
    max_data = max(data_list)

    # 定义生成文件名称
    file_name = 'China_railway_bureau_map(normal).html'
    # 定义地图参数
    map = (
        # 定义尺寸等初始设置
        Map(init_opts=opts.InitOpts(width='1000px', height='750px', bg_color='white', page_title='各路局地图'))
        # 注册地图
        .add_js_funcs("echarts.registerMap('china_railway', {});".format(json_data))
        .add(
            # 系列名称
            series_name='设备数量',
            # 数据项(坐标点名称，坐标点值)
            data_pair=bureau_data,
            # 地图类型，新注册的题图
            maptype='china_railway',
            # 是否开启鼠标缩放和平移漫游
            is_roam=True,
            # 当前视角的缩放比例。
            zoom=1,
            # 是否显示标记图形，False=取消红点显示
            is_map_symbol_show=True,
            )
        # False=取消路局名称显示
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title='中国各路局设备数量分布'),
            visualmap_opts=opts.VisualMapOpts(
                min_=min_data,
                max_=max_data,
                # 两端的文本
                range_text=['最大值', '最小值'],
                # visualMap 组件过渡颜色
                range_color=['lightskyblue', 'yellow', 'orangered']
                ),
            toolbox_opts=opts.ToolboxOpts(
                # 是否显示该工具 True=显示
                is_show=True,
                # 工具栏的布局朝向:横向
                orient='horizontal',
                # 工具栏离底侧像素5
                pos_bottom='5',
                # 工具栏只显示保存图片的功能
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True, name=file_name[:-5]),
                    restore=opts.ToolBoxFeatureRestoreOpts(is_show=False),
                    data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                    magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=False),
                    brush=opts.ToolBoxFeatureBrushOpts(type_=False)
                )
            )
        )
    )
    map.render('{0}'.format(file_name))
    print('文件{0}已生成至当前路径下!'.format(file_name))


def heat_signal_color_map(bureau_data, reduction_factor=5, symbol_color='#ff0000'):
    """
    热力地图-单色
    :param bureau_data: 路局名称和数据的list [['沈阳局', 100],...]
    :param reduction_factor: 图标根据实际值缩放的大小，默认=5
    :param symbol_color: 图标显示的颜色，默认红色
    :return: 生成html文件，无返回值
    """
    # 判断json数据是否为空，也就是检查json文件是否存在
    json_data = china_railway_bureau_map

    # 用原生JS来计算圆形的尺寸
    get_symbol_size = 'function (val) {return val[2]/' + '{0};'.format(reduction_factor) + '}'

    file_name = 'China_railway_bureau_map(heat_signal_color).html'
    heat_map = (
        Geo(init_opts=opts.InitOpts(width='1000px', height='750px', bg_color='white', page_title='各路局热力地图'))
        .add_js_funcs("echarts.registerMap('china_railway', {});".format(json_data))
        .add_schema(maptype="china_railway")
        .set_global_opts(
            title_opts=opts.TitleOpts(title='中国各路局设备数量分布热力图'),
            toolbox_opts=opts.ToolboxOpts(
                # 是否显示该工具 True=显示
                is_show=True,
                # 工具栏的布局朝向:横向
                orient='horizontal',
                # 工具栏离底侧像素5
                pos_bottom='5',
                # 工具栏只显示保存图片的功能
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True, name=file_name[:-5]),
                    restore=opts.ToolBoxFeatureRestoreOpts(is_show=False),
                    data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                    magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=False),
                    brush=opts.ToolBoxFeatureBrushOpts(type_=False)
                )
            )
        )
    )
    # 获取路局中心坐标点
    center_coordinate_dict = get_center_coordinate()
    # 增加坐标点
    for item in bureau_data:
        if item[0] in center_coordinate_dict:
            # 当数据的名称是规定的路径名称，数据才会增加到地图上
            heat_map.add_coordinate(name=item[0],
                                    longitude=center_coordinate_dict[item[0]][0],
                                    latitude=center_coordinate_dict[item[0]][1])
    heat_map.add(
        series_name='',
        data_pair=bureau_data,
        type_=ChartType.EFFECT_SCATTER,
        # 尺寸定义
        symbol_size=JsCode(get_symbol_size),
        color=symbol_color
    )
    heat_map.set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter='{b}'))
    heat_map.render('{0}'.format(file_name))
    print('文件{0}已生成至当前路径下!'.format(file_name))


def heat_mult_color_map(bureau_data, display_type='effect'):
    """
    热力地图-多种颜色
    :param bureau_data: 路局名称和数据的list
    :param display_type: 显示效果EFFECT_SCATTER or HEATMAP
    :return: 生成html文件，无返回值
    """
    json_data = china_railway_bureau_map

    # 计算传入数据的最大值和最小值，用于颜色显示标签
    data_list = [item[1] for item in bureau_data]
    min_data = min(data_list)
    max_data = max(data_list)

    if display_type == 'effect':
        display_type = ChartType.EFFECT_SCATTER
    else:
        display_type = ChartType.HEATMAP
    file_name = 'China_railway_bureau_map(heat_mult_color).html'
    heat_map = (
        Geo(init_opts=opts.InitOpts(width='1000px', height='750px', bg_color='white', page_title='各路局热力地图'))
        .add_js_funcs("echarts.registerMap('china_railway', {});".format(json_data))
        .add_schema(maptype="china_railway")
        .set_global_opts(
            title_opts=opts.TitleOpts(title='中国各路局设备数量分布热力图'),
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                min_=min_data,
                max_=max_data,
                # 两端的文本
                range_text=['最大值', '最小值'],
                # visualMap 组件过渡颜色
                range_color=['lightskyblue', 'yellow', 'orangered']
            ),
            toolbox_opts=opts.ToolboxOpts(
                # 是否显示该工具 True=显示
                is_show=True,
                # 工具栏的布局朝向:横向
                orient='horizontal',
                # 工具栏离底侧像素5
                pos_bottom='5',
                # 工具栏只显示保存图片的功能
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True, name=file_name[:-5]),
                    restore=opts.ToolBoxFeatureRestoreOpts(is_show=False),
                    data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                    magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=False),
                    brush=opts.ToolBoxFeatureBrushOpts(type_=False)
                )
            )
        )
    )
    # 获取路局中心坐标点
    center_coordinate_dict = get_center_coordinate()
    # 增加坐标点
    for item in bureau_data:
        if item[0] in center_coordinate_dict:
            # 当数据的名称是规定的路径名称，数据才会增加到地图上
            heat_map.add_coordinate(name=item[0],
                                    longitude=center_coordinate_dict[item[0]][0],
                                    latitude=center_coordinate_dict[item[0]][1])
    heat_map.add(
        series_name='',
        data_pair=bureau_data,
        type_=display_type,
        # 尺寸定义
        symbol_size=25
    )
    heat_map.set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter='{b}'))
    heat_map.render('{0}'.format(file_name))
    print('文件{0}已生成至当前路径下!'.format(file_name))


def single_bureau_map(bureau_name, data=None, reduction_factor=5, symbol_color='#ff0000'):
    """
    单独路局地图
    :param bureau_name: 路局名称和数据的list
    :param data: 单个路局地图对应的输入数据，字典格式
    :param reduction_factor: 圆形符号根据每个点真实数字的缩小比例，默认缩小5倍
    :param symbol_color: 圆形符号的颜色，默认红色
    :return: 生成html文件，无返回值
    """
    # 判断输入的名字是否在列表中
    bureau_name_list = ['haerbinju', 'shenyangju', 'huhehaoteju', 'beijingju', 'wulumuqiju',
                        'qingzanggongsi', 'chengduju', 'kunmingju', 'lanzhouju', 'xianju',
                        'taiyuanju', 'zhengzhouju', 'jinanju', 'shanghaiju', 'nanchangju',
                        'guangzhouju', 'nanningju', 'wuhanju']
    if bureau_name not in bureau_name_list:
        # 输入的名字不在所有路局名字列表中，则退出
        print('"{0}"路局名称不正确，程序无法执行!'.format(bureau_name))
        return
    json_data = eval(bureau_name)

    # 当没有数据的时候，绘制的是空白的地图，只有数据不为none的时候，根据数据内容绘制地图
    flag = 0
    if data is not None:
        # 用原生JS来计算圆形的尺寸
        get_symbol_size = 'function (val) {return val[2]/' + '{0};'.format(reduction_factor) + '}'
        # 根据data获取坐标和数量，用于后面绘图
        data_name_coordinate_list = []
        data_name_num_list = []
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and 'coord' in value and 'num' in value:
                    data_name_coordinate_list.append([key, value['coord'][0], value['coord'][1]])
                    data_name_num_list.append([key, value['num']])
                    flag = 1
                else:
                    print('"{0}"数据格式不满足要求(不是字典或者键值缺少“coord”或“num”)！'.format(key))

        else:
            print('输入数据"data"不是字典格式!')

    file_name = '{0}_map.html'.format(bureau_name)
    heat_map = (
        Geo(init_opts=opts.InitOpts(width='1000px', height='750px', bg_color='white', page_title='{}地图'.format(
            bureau_name)))
        .add_js_funcs("echarts.registerMap('{0}', {1});".format(bureau_name, json_data))
        .add_schema(maptype='{0}'.format(bureau_name))
        .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(
                # 是否显示该工具 True=显示
                is_show=True,
                # 工具栏的布局朝向:横向
                orient='horizontal',
                # 工具栏离底侧像素5
                pos_bottom='5',
                # 工具栏只显示保存图片的功能
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(is_show=True, name=file_name[:-5]),
                    restore=opts.ToolBoxFeatureRestoreOpts(is_show=False),
                    data_view=opts.ToolBoxFeatureDataViewOpts(is_show=False),
                    data_zoom=opts.ToolBoxFeatureDataZoomOpts(is_show=False),
                    magic_type=opts.ToolBoxFeatureMagicTypeOpts(is_show=False),
                    brush=opts.ToolBoxFeatureBrushOpts(type_=False)
                )
            )
        )
    )
    if flag == 1:
        # 增加坐标点
        for item in data_name_coordinate_list:
            heat_map.add_coordinate(name=item[0], longitude=item[1], latitude=item[2])
        # 增加坐标点以后，绘制相关标注点
        heat_map.add(
            series_name='',
            data_pair=data_name_num_list,
            type_=ChartType.EFFECT_SCATTER,
            # 尺寸定义
            symbol_size=JsCode(get_symbol_size),
            color=symbol_color
        )
        # 这个设置需要在这里设置，在前面设置不起作用
        heat_map.set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter='{b}'))

    heat_map.render('{0}'.format(file_name))
    print('文件{0}已生成至在当前路径下!'.format(file_name))
