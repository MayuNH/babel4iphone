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


#ifndef __CHARACTER_H__
#define __CHARACTER_H__

#import "SharedData.h"

@interface Character : NSObject 
{
	int uid;
	NSString* name;
	int pos;
	NSString* race;
	NSString* job;
	int level;
	int exp;
	NSString* supjob;
	int suplevel;
	int maxHp;
	int maxMp;
	int hp;
	int mp;
	int str;
	int dex;
	int vit;
	int agi;
	int inte;
	int mnd;
}

@property (nonatomic, readwrite) int uid;
@property (nonatomic, readwrite, retain) NSString* name;
@property (nonatomic, readwrite) int pos;
@property (nonatomic, readwrite, retain) NSString* race;
@property (nonatomic, readwrite, retain) NSString* job;
@property (nonatomic, readwrite) int level;
@property (nonatomic, readwrite) int exp;
@property (nonatomic, readwrite, retain) NSString* supjob;
@property (nonatomic, readwrite) int suplevel;
@property (nonatomic, readwrite) int maxHp;
@property (nonatomic, readwrite) int maxMp;
@property (nonatomic, readwrite) int hp;
@property (nonatomic, readwrite) int mp;
@property (nonatomic, readwrite) int str;
@property (nonatomic, readwrite) int dex;
@property (nonatomic, readwrite) int vit;
@property (nonatomic, readwrite) int agi;
@property (nonatomic, readwrite) int inte;
@property (nonatomic, readwrite) int mnd;

-(id) initWithInfo:(NSArray *)baseInfo position:(int)p;

+(id) charWithInfo:(NSArray *)baseInfo position:(int)p;

@end

#endif
