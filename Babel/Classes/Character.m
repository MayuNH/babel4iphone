// This file is part of babel4iphone.

// Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>

// babel4iphone is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// babel4iphone is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with babel4iphone.  If not, see <http://www.gnu.org/licenses/>.


#import "Character.h"
#import "SharedData.h"

@implementation Character

@synthesize uid, name, pos, race, job, level, exp, supjob, suplevel, maxHp, maxMp, hp, mp, str, dex, vit, agi, inte, mnd;

+(id) charWithInfo:(NSArray *)baseInfo position:(int)p
{
	return [[[self alloc] initWithInfo:baseInfo position:p] autorelease];
}

-(id) initWithInfo:(NSArray *)baseInfo position:(int)p
{
    if ((self = [super init]))
	{
		self.pos = p;
		
		self.uid = [[baseInfo objectAtIndex:0] intValue];
		self.name = [baseInfo objectAtIndex:1];
		self.race = [baseInfo objectAtIndex:2];
		self.job = [baseInfo objectAtIndex:3];
		self.supjob = [baseInfo objectAtIndex:4];
		
		self.level = [[baseInfo objectAtIndex:5] intValue];
		self.suplevel = 0;
		if ([baseInfo count] > 10)
			self.suplevel = [[baseInfo objectAtIndex:10] intValue];
		
		self.exp = [[baseInfo objectAtIndex:6] intValue];
		
		NSMutableArray *extraInfo = [[SharedData Initialize] getCharInfo:self.race 
																	 job:self.job
																   level:self.level
																  supjob:self.supjob
																suplevel:self.suplevel];
		
		NSLog(@"-----> %@", baseInfo);
		NSLog(@"-----> %@", extraInfo);
		
		self.maxHp = [[extraInfo objectAtIndex:0] intValue];
		self.maxMp = [[extraInfo objectAtIndex:1] intValue];
		self.str = [[extraInfo objectAtIndex:2] intValue];
		self.dex = [[extraInfo objectAtIndex:3] intValue];
		self.vit = [[extraInfo objectAtIndex:4] intValue];
		self.agi = [[extraInfo objectAtIndex:5] intValue];
		self.inte = [[extraInfo objectAtIndex:6] intValue];
		self.mnd = [[extraInfo objectAtIndex:7] intValue];
		
		double timestamp = [[baseInfo objectAtIndex:9] doubleValue];
		NSLog(@"timestamp %f", timestamp);
		
		self.hp = [[baseInfo objectAtIndex:7] intValue];
		self.mp = [[baseInfo objectAtIndex:8] intValue];
	}
	
    return self;
}

// on "dealloc" you need to release all your retained objects
-(void) dealloc
{	
	[name release];
	[race release];
	[job release];
	[supjob release];
	
	NSLog(@"-----------> Release Character");
	
	// in case you have something to dealloc, do it in this method
	// in this particular example nothing needs to be released.
	// cocos2d will automatically release all the children (Label)
	
	// don't forget to call "super dealloc"
	[super dealloc];
}

@end
