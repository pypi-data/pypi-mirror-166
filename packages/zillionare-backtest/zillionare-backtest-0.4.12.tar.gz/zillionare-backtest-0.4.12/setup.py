# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backtest',
 'backtest.common',
 'backtest.config',
 'backtest.feed',
 'backtest.trade',
 'backtest.web',
 'tests',
 'tests.common',
 'tests.feed',
 'tests.trade',
 'tests.web']

package_data = \
{'': ['*'], 'tests': ['data/*']}

install_requires = \
['aioredis==1.3.1',
 'arrow>=1.2.2,<2.0.0',
 'async-timeout>=4.0,<5.0',
 'cfg4py>=0.9.4,<0.10.0',
 'expiringdict>=1.2.1,<2.0.0',
 'fire==0.4.0',
 'httpx>=0.23.0,<0.24.0',
 'pandas>=1.4.1,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'pyemit==0.4.5',
 'sanic>=21.12.1,<22.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.63.0,<5.0.0',
 'zillionare-core-types>=0.5.2,<0.6.0',
 'zillionare-omicron>=2.0.0.a42,<3.0.0']

extras_require = \
{'dev': ['black>=22.3.0,<23.0.0',
         'isort==5.10.1',
         'flake8==4.0.1',
         'flake8-docstrings>=1.6.0,<2.0.0',
         'tox>=3.24.5,<4.0.0',
         'virtualenv>=20.13.1,<21.0.0',
         'twine>=3.8.0,<4.0.0',
         'pre-commit>=2.17.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0',
         'livereload>=2.6.3,<3.0.0',
         'mike>=1.1.2,<2.0.0',
         'Jinja2>=3.0,<3.1'],
 'test': ['pytest>=7.0.1,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'sanic-testing>=0.8.2,<0.9.0']}

entry_points = \
{'console_scripts': ['bt = backtest.cli:main']}

setup_kwargs = {
    'name': 'zillionare-backtest',
    'version': '0.4.12',
    'description': 'zillionare backtest framework.',
    'long_description': '[![Version](http://img.shields.io/pypi/v/zillionare-backtest?color=brightgreen)](https://pypi.python.org/pypi/zillionare-backtest)\n[![CI Status](https://github.com/zillionare/backtesting/actions/workflows/release.yml/badge.svg)](https://github.com/zillionare/backtesting)\n[![Code Coverage](https://img.shields.io/codecov/c/github/zillionare/backtesting)](https://app.codecov.io/gh/zillionare/backtesting)\n[![Downloads](https://pepy.tech/badge/zillionare-backtest)](https://pepy.tech/project/zillionare-backtest)\n[![License](https://img.shields.io/badge/License-MIT.svg)](https://opensource.org/licenses/MIT)\n[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)\n# zillionare-backtest\n\nzillionare-backtest是大富翁的回测服务器，它跟[zillionare-omega](https://zillionare.github.io/omega/), [zillionare-omicron](https://zillionare.github.io/omicron), [zillionare-alpha](https://zillionare.github.io/alpha), [zillionare-trader-client](https://zillionare.github.io/traderclient)共同构成回测框架。\n\nzillionare-backtest的功能是提供账户管理、交易撮合和策略评估。zillionare-backtest使用omicron来提供撮合数据，但您也可以自写开发撮合数据的提供器[^1]。\n\n与普通的回测框架不同，大富翁回测框架并非是侵入式的。在您的策略中，只需要接入我们的trader-client,并在策略发出交易信号时，向backtest server发出对应的交易指令，即可完成回测。当回测完成，转向实盘时，不需要修改策略代码，仅需要指回测服务器url指向[zillionare-trader-server](https://zillionare.github.io/traderserver/)即可。zillionare-backtest与zillionare-trader-server的API绝大多数地方是完全兼容的。\n\n这种设计意味着，您的策略可以不使用大富翁数据框架，甚至可以不使用zillionare-trader-client（您可以自定义一套接口并实现，使之能同时适配您的交易接口和backtest接口）。因此，您的策略可以在任何时候，切换到最适合的量化框架。\n\n# 功能\n## 账户管理\n当您开始回测时，先通过[start_backtest][backtest.web.interfaces.start_backtest]来创建一个账户。在知道该账户的`name`与`token`的情况下，您可以在随后通过[delete_accounts][backtest.web.interfaces.delete_accounts]来删除账户。\n\n## 交易撮合\n\n您可以通过[buy][backtest.web.interfaces.buy], [market_buy][backtest.web.interfaces.market_buy], [sell][backtest.web.interfaces.sell], [market_sell][backtest.web.interfaces.market_sell]和[sell_percent][backtest.web.interfaces.sell_percent]来进行交易。\n\n## 状态跟踪\n\n您可以通过[info][backtest.web.interfaces.info]来查看账户的基本信息，比如当前总资产、持仓、本金、盈利等。您还可以通过[positions][backtest.web.interfaces.positions]、[bills][backtest.web.interfaces.bills]来查看账户的持仓、交易历史记录\n## 策略评估\n\n[metrics][backtest.web.interfaces.metrics]方法将返回策略的各项指标，比如sharpe, sortino, calmar, win rate, max drawdown等。您还可以传入一个参考标的，backtest将对参考标的也同样计算上述指标。\n\n# 关键概念\n\n## 复权处理\n您的策略在发出买卖信号时，应该使用与`order_time`一致的现价，而不是任何复权价。如果您的持仓在持有期间，发生了分红送股，回测服务器会自动将分红送股转换成股数加到您的持仓中。当您最终清空持仓时，可以通过`bills`接口查询到分红送股的成交情况（记录为XDXR类型的委托）。\n\n## 撮合机制\n在撮合时，backtest首先从data feeder中获取`order_time`以后（含）的行情数据。接下来去掉处在涨跌停中的那些bar（如果是委买，则去掉已处在涨停期间的bar，反之亦然）。在剩下的bar中，backtest会选择价格低于委托价的那些bar（如果是委卖，则选择价格高于委托价的那些bar）,依顺序匹配委托量，直到委托量全部被匹配为止。最后，backtest将匹配到的bar的量和价格进行加权平均，得到成交均价。\n\n当backtest使用zillionare-feed来提供撮合数据时，由于缺少盘口数据，zillionare-feed使用分钟级行情数据中的`close`价格和`volume`来进行撮合。因此，可能出现某一分钟的最高价或者最低价可能满足过您的委托价要求，但backtest并未成交撮合的情况。我们这样设计，主要考虑到当股价达到最高或者最低点时，当时的成交量不足以满足委托量。现在backtest的设计，可能策略的鲁棒性更好。\n\n作为一个例外，如果委托时的`order_time`为9:31分之前，backtest将会使用9:31分钟线的开盘价，而不是9:31分的收盘价来进行撮合，以满足部分策略需要以**次日开盘价**买入的需求。\n\n另外，您也应该注意到，zillionare-feed使用分钟线来替代了盘口数据，尽管在绝大多数情形下，这样做不会有什么影响，但两者毕竟是不同的。一般来说，成交量肯定小于盘口的委买委卖量。因此，在回测中出现买卖委托量不足的情况时，对应的实盘则不一定出现。在这种情况下，可以适当调低策略的本金设置。另外一个差异是，分钟成交价必然不等同于盘口成交价，因此会引入一定的误差。不过长期来看，这种误差应该是零均值的，因此对绝大多数策略不会产生实质影响。\n\n!!!info\n    了解backtest的撮合机制后，您应该已经明白，正确设定策略的本金(`principal`)会使得回测的系统误差更小。\n\n## 委买委卖\n委买时，委买量必须是100股的整数倍。这个限制与实盘是一致的。同样，您的券商对委卖交易也做了限制，但回测服务器并未对此进行限制。经评估，去掉这个限制并不会对策略的有效性产生任何影响，但会简化策略的编写。\n\n## 停牌处理\n如果某支持仓股当前停牌，在计算持仓市值时，系统会使用停牌前的收盘价来计算市值。为性能优化考验，如果一支股票停牌时间超过500个交易日，则系统将放弃继续向前搜索停牌前的收盘价，改用买入时的成交均价来代替。这种情况应该相当罕见。\n# 版本历史\n关于版本历史，请查阅[版本历史](history)\n# Credits\n\nZillionare-backtest项目是通过[Python Project Wizard](zillionare.github.io/python-project-wizard)创建的。\n\n\n[^1]:此功能在0.4.x版本中尚不可用。\n',
    'author': 'Aaron Yang',
    'author_email': 'aaron_yang@jieyu.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zillionare/backtest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
