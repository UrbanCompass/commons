# ==================================================================================================
# Copyright 2011 Twitter, Inc.
# --------------------------------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==================================================================================================

from glob import glob


java_tests(name = 'memcached',
  dependencies = [
    '3rdparty:guava',
    '3rdparty:junit',
    '3rdparty:thrift',
    'src/java/com/twitter/common/io:thrift',
    'src/java/com/twitter/common/memcached:thrift-transcoder',
    'src/java/com/twitter/common/thrift:testing',
  ],
  sources = glob('*.java')
)
