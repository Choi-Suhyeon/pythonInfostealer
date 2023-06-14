# 첫 commit 전 시행착오

1. 처음에는 log를 기록할 때, thread를 이용해, 한 thread에서 10초마다 log가 차있다면, 저장을 시키고, log를 비우는 방식을 사용했다. 하지만 코드가 생각보다 많이 복잡해졌다.
1. stream을 이용했다. 코드는 간단해졌지만, 중간에 갑자기 종료됐을 때 저장이 되지 않았다.
1. 프로그램이 끝날 때 코드를 실행시킬 방법을 찾던 중 atexit을 찾았다.

문제는 Ctrl+C로 종료하면, atexit.register가 실행되지만, cmd나 powershell에서 Ctrl+Break로 종료하면 실행이 되지 않고 프로그램이 종료된다.