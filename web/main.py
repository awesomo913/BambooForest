"""Pygbag entry point -- delegates to game.main()."""

import asyncio

from game import main

asyncio.run(main())
